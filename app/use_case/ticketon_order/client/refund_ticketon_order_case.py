from datetime import datetime
from typing import Any, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_cancel_payment_dto import AlatauCancelPaymentDTO
from app.adapters.dto.alatau.alatau_cancel_payment_response_dto import AlatauRefundPaymentResultDTO
from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.alatau.alatau_status_request_dto import AlatauStatusRequestDTO
from app.adapters.dto.alatau.alatau_status_response_dto import AlatauPaymentStatusResponseDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, \
    PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingShowBookingDTO
from app.adapters.dto.ticketon.ticketon_refund_dto import TicketonRefundDTO
from app.adapters.dto.ticketon.ticketon_refund_request_dto import TicketonSaleRefundResponseDTO
from app.adapters.dto.ticketon.ticketon_response_for_sale_dto import TicketonResponseForSaleDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO, TicketonOrderCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.adapters.repository.ticketon_order_and_payment_transaction.ticketon_order_and_payment_transaction_repository import \
    TicketonOrderAndPaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionEntity, TicketonOrderEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.alatau_service.alatau_service_api import AlatauServiceAPI
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class RefundTicketonOrderCase(BaseUseCase[TicketonResponseForSaleDTO]):
    """
    Use Case для возврата билета Ticketon с обработкой платежной транзакции.
    
    АЛГОРИТМ РАБОТЫ:
    ================
    1. ПРОВЕРКА ЗАКАЗА:
       - Оплачен и подтвержден → отменить в Ticketon, затем возврат в Алатау
       - Отменен и ожидает возврата → только возврат в Алатау (уже отменен в Ticketon)
    
    2. ОБРАБОТКА ПЛАТЕЖНОЙ ТРАНЗАКЦИИ:
       - Проверить актуальный статус в банке
       - Если оплачен → запросить возврат, обновить статус на "Средства возвращены"
       - Если ожидает возврата → проверить статус и обновить
       - Если уже возвращен → просто обновить статус заказа
    
    СТАТУСЫ ЗАКАЗА:
    - PaidConfirmed → CancelledAwaitingRefund/CancelledRefunded
    - CancelledAwaitingRefund → CancelledRefunded
    
    СТАТУСЫ ТРАНЗАКЦИИ:
    - Paid → Refunded (через банк)
    - AwaitingRefund → Refunded (проверка банка)
    """

    def __init__(self, db: AsyncSession) -> None:
        # Репозитории для работы с данными
        self.ticketon_repository = TicketonOrderRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.ticketon_order_and_payment_transaction_repository = TicketonOrderAndPaymentTransactionRepository(db)
        # Внешние API сервисы
        self.alatau_service_api = AlatauServiceAPI()
        self.ticketon_service_api = TicketonServiceAPI()
        
        # Рабочие данные (инициализируются в execute)
        self.active_ticketon_order: TicketonOrderEntity | None = None
        self.active_payment_transaction: PaymentTransactionEntity | None = None
        self.sale: str | None = None
        self.user: UserWithRelationsRDTO | None = None
        
        # DTO для ответа (инициализируется в execute)
        self.common_response_dto: TicketonRefundDTO | None = None
        self.current_time = datetime.now()

    async def execute(self, sale: str, user: UserWithRelationsRDTO | None = None) -> TicketonResponseForSaleDTO:
        """
        Основной метод выполнения возврата билета.
        
        Args:
            sale: Номер продажи (sale) в системе Ticketon
            user: Пользователь, инициирующий возврат (опционально)
            
        Returns:
            TicketonResponseForSaleDTO: Результат операции возврата
        """
        # Инициализация параметров
        self.user = user
        self.sale = sale
        
        # Инициализация DTO для ответа
        self.common_response_dto = TicketonRefundDTO()
        
        # Валидация и загрузка базовых данных
        await self.validate()
        
        # Выполнение основной логики возврата
        await self.transform()
        
        # Повторная загрузка данных с связями для финального ответа
        # (данные могли измениться в transform)
        updated_order = await self.ticketon_repository.get_first_with_filters(
            filters=[self.ticketon_repository.model.sale == self.sale],
            include_deleted_filter=True,
            options=self.ticketon_repository.default_relationships()
        )
        
        updated_transaction = await self.payment_transaction_repository.get_first_with_filters(
            filters=[
                or_(
                    self.payment_transaction_repository.model.order == self.sale,
                    self.payment_transaction_repository.model.id == updated_order.payment_transaction_id,
                )
            ],
            include_deleted_filter=True,
            options=self.payment_transaction_repository.default_relationships()
        )
        
        # Формирование финального ответа
        # Используем безопасное создание DTO - relationships уже загружены через default_relationships()
        self.common_response_dto.ticketon_order = TicketonOrderWithRelationsRDTO.model_validate(updated_order)
        self.common_response_dto.payment_transaction = PaymentTransactionWithRelationsRDTO.model_validate(updated_transaction)
        
        return self.common_response_dto

    async def validate(self):
        """
        Валидация входных данных и загрузка необходимых сущностей.
        
        Проверяет:
        1. Существование заказа Ticketon
        2. Статус оплаты заказа
        3. Допустимые статусы для возврата
        4. Существование платежной транзакции
        """
        # Загрузка заказа Ticketon
        self.active_ticketon_order = await self.ticketon_repository.get_first_with_filters(
            filters=[self.ticketon_repository.model.sale == self.sale],
            include_deleted_filter=True
        )
        
        # Проверка существования заказа
        if not self.active_ticketon_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_not_found"))
        
        # Проверка статуса оплаты
        if not self.active_ticketon_order.is_paid or self.active_ticketon_order.payment_transaction_id is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_not_paid"))
        
        # ИСПРАВЛЕНА КРИТИЧЕСКАЯ ОШИБКА: изменен OR на AND
        # Заказ должен быть либо подтвержден, либо отменен и ожидает возврата
        allowed_statuses = [
            DbValueConstants.TicketonOrderStatusPaidConfirmedID,
            DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID
        ]
        if self.active_ticketon_order.status_id not in allowed_statuses:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_order_is_not_confirmed_or_cancelled")
            )
        
        # Проверка, что возврат еще не был произведен
        if self.active_ticketon_order.status_id == DbValueConstants.TicketonOrderStatusCancelledRefundedID:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_already_refunded"))

        # Проверка связи
        ticketon_order_and_payment_transaction = await self.ticketon_order_and_payment_transaction_repository.get_first_with_filters(
            filters=[
                self.ticketon_order_and_payment_transaction_repository.model.ticketon_order_id == self.active_ticketon_order.id,
                self.ticketon_order_and_payment_transaction_repository.model.is_active.is_(True)
            ],
            include_deleted_filter=True
        )
        if not ticketon_order_and_payment_transaction:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))
        # Загрузка платежной транзакции
        self.active_payment_transaction = await self.payment_transaction_repository.get_first_with_filters(
            filters=[
                or_(
                    self.payment_transaction_repository.model.id == ticketon_order_and_payment_transaction.payment_transaction_id,
                    self.payment_transaction_repository.model.id == self.active_ticketon_order.payment_transaction_id,
                )
            ],
            include_deleted_filter=True
        )
        
        # Проверка существования транзакции
        if not self.active_payment_transaction:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))

    async def transform(self):
        """
        Основная логика обработки возврата в зависимости от статуса заказа.
        
        СЦЕНАРИИ:
        1. PaidConfirmed → отмена в Ticketon + возврат через банк
        2. CancelledAwaitingRefund → только возврат через банк (уже отменен в Ticketon)
        """
        # СЦЕНАРИЙ 1: Заказ оплачен и подтвержден - нужна отмена в Ticketon
        if self.active_ticketon_order.status_id == DbValueConstants.TicketonOrderStatusPaidConfirmedID:
            # Отмена бронирования в системе Ticketon
            ticketon_refund_response: TicketonSaleRefundResponseDTO = await self.ticketon_service_api.sale_refund(
                self.active_ticketon_order.sale
            )
            
            # Проверка ответа от Ticketon
            if ticketon_refund_response.status == 0:
                # Ошибка в Ticketon - прерываем операцию
                raise AppExceptionResponse.bad_request(message=ticketon_refund_response.error)
            
            # Ticketon успешно отменил бронирование
            if ticketon_refund_response.status == 1:
                # Обрабатываем возврат денежных средств
                refund_result: Tuple[int, bool, str] = await self._process_payment_refund()
                
                # Создаем DTO для обновления заказа (избегаем проблем с relationship)
                ticketon_update_dto = self._create_safe_ticketon_update_dto(
                    status_id=refund_result[0],
                    is_canceled=True,
                    cancel_reason="Отменено пользователем, возврат средств в обработке"
                )
                
                # Сохраняем изменения в заказе
                await self.ticketon_repository.update(obj=self.active_ticketon_order, dto=ticketon_update_dto)
                
                # Записываем результат в DTO ответа
                self.common_response_dto.status = refund_result[1]
                self.common_response_dto.error_message = refund_result[2]
        
        # СЦЕНАРИЙ 2: Заказ уже отменен в Ticketon, ожидает возврата средств
        elif self.active_ticketon_order.status_id == DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID:
            # Обрабатываем возврат денежных средств
            refund_result: Tuple[int, bool, str] = await self._process_payment_refund()
            
            # Создаем DTO для обновления заказа (избегаем проблем с relationship)
            ticketon_update_dto = self._create_safe_ticketon_update_dto(
                status_id=refund_result[0],
                is_canceled=True,
                cancel_reason="Возврат средств в обработке"
            )
            
            # Сохраняем изменения
            await self.ticketon_repository.update(obj=self.active_ticketon_order, dto=ticketon_update_dto)
            
            # Записываем результат в DTO ответа
            self.common_response_dto.status = refund_result[1]
            self.common_response_dto.error_message = refund_result[2]

    async def _process_payment_refund(self) -> Tuple[int, bool, str]:
        """
        Обработка возврата денежных средств через банк Алатау.
        
        АЛГОРИТМ:
        1. Проверить текущий статус в банке
        2. В зависимости от статуса транзакции:
           - Paid → запросить возврат
           - AwaitingRefund → проверить статус возврата
           - Refunded → подтвердить завершение
           
        Returns:
            Tuple[int, bool, str]: (новый_статус_заказа, успех_операции, сообщение)
        """
        payment_update_dto = self._create_safe_payment_transaction_update_dto()
        
        # Сначала всегда проверяем актуальный статус в банке
        bank_status_result: Optional[Tuple[int, bool, str]] = await self._check_bank_payment_status(payment_update_dto)
        if bank_status_result is not None:
            return bank_status_result
        
        # Обработка в зависимости от статуса транзакции
        current_status = self.active_payment_transaction.status_id
        
        # СЛУЧАЙ 1: Транзакция оплачена - инициируем возврат
        if current_status == DbValueConstants.PaymentTransactionStatusPaidID:
            return await self._initiate_refund(payment_update_dto)
        
        # СЛУЧАЙ 2: Возврат уже инициирован - проверяем статус
        elif current_status == DbValueConstants.PaymentTransactionStatusAwaitingRefundID:
            bank_check_result = await self._check_bank_payment_status(payment_update_dto)
            if bank_check_result is not None:
                return bank_check_result
            else:
                # Статус не изменился - остается в ожидании
                return (
                    DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                    False,
                    i18n.gettext("refund_still_processing")
                )
        
        # СЛУЧАЙ 3: Возврат уже произведен
        elif current_status == DbValueConstants.PaymentTransactionStatusRefundedID:
            return (
                DbValueConstants.TicketonOrderStatusCancelledRefundedID,
                True,
                i18n.gettext("ticketon_order_is_already_refunded")
            )
        
        # СЛУЧАЙ 4: Неожиданный статус
        else:
            return (
                DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                False,
                f"Неожиданный статус транзакции: {current_status}"
            )
    
    async def _initiate_refund(self, payment_update_dto: PaymentTransactionCDTO) -> Tuple[int, bool, str]:
        """
        Инициирует возврат средств через API Алатау.
        
        Returns:
            Tuple[int, bool, str]: Результат операции возврата
        """
        # Подготовка запроса на возврат
        refund_request_dto = AlatauCancelPaymentDTO()
        refund_request_dto.ORDER = self.active_payment_transaction.order
        refund_request_dto.REV_AMOUNT = float(self.active_payment_transaction.amount)
        refund_request_dto.REV_DESC = "Отмена заказа билетов по запросу пользователя"
        
        # Выполнение запроса на возврат
        refund_response: AlatauRefundPaymentResultDTO = await self.alatau_service_api.payment_refund(
            refund_request_dto
        )
        
        # Обработка ответа от банка
        if refund_response.code == 0:  # Успешный возврат
            # Обновляем транзакцию как возвращенную
            payment_update_dto.status_id = DbValueConstants.PaymentTransactionStatusRefundedID
            
            # Извлекаем данные из operation, если она доступна
            if refund_response.operation:
                payment_update_dto.rev_amount = refund_response.operation.amount
                payment_update_dto.rev_desc = refund_response.operation.rev_desc
            else:
                # Если operation недоступна, используем данные из основного запроса
                payment_update_dto.rev_amount = self.active_payment_transaction.amount
                payment_update_dto.rev_desc = refund_response.description or "Возврат выполнен"
                
            payment_update_dto.is_canceled = True
            
            await self.payment_transaction_repository.update(
                obj=self.active_payment_transaction,
                dto=payment_update_dto
            )
            
            return (
                DbValueConstants.TicketonOrderStatusCancelledRefundedID,
                True,
                refund_response.description or "Возврат выполнен успешно"
            )
        else:  # Ошибка возврата
            # Переводим в статус ожидания возврата
            payment_update_dto.status_id = DbValueConstants.PaymentTransactionStatusAwaitingRefundID
            payment_update_dto.rev_desc = refund_response.description or "Возврат в обработке"
            
            await self.payment_transaction_repository.update(
                obj=self.active_payment_transaction,
                dto=payment_update_dto
            )
            
            return (
                DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                False,
                refund_response.description or "Ошибка при обработке возврата"
            )

    async def _check_bank_payment_status(self, payment_update_dto: PaymentTransactionCDTO) -> Optional[Tuple[int, bool, str]]:
        """
        Проверка текущего статуса платежа в банке Алатау.
        
        Анализирует статус возврата и обновляет транзакцию при необходимости.
        
        Args:
            payment_update_dto: DTO для обновления транзакции
            
        Returns:
            Optional[Tuple[int, bool, str]]: Результат если статус изменился, None если нет изменений
        """
        try:
            # Запрос статуса платежа у банка
            status_request = AlatauStatusRequestDTO()
            status_request.ORDER = self.active_payment_transaction.order
            
            bank_status_response: AlatauPaymentStatusResponseDTO = await self.alatau_service_api.get_payment_status(status_request)
            
            # Проверка успешности запроса
            if bank_status_response.code != 0 or bank_status_response.operation is None:
                return None  # Нет данных о статусе
            
            # Анализ основного статуса операции
            if bank_status_response.operation.status != "S":  # Не "Success"
                return None  # Операция не завершена успешно
            
            # Проверка наличия данных о возвратах
            if bank_status_response.operation.refunds is None or not bank_status_response.operation.refunds.records:
                return None  # Нет информации о возвратах
            
            # Анализ записей возвратов (берем последнюю по времени)
            for refund_record in bank_status_response.operation.refunds.records:
                
                # УСПЕШНЫЙ ВОЗВРАТ
                if refund_record.status == "R":  # Refunded - возврат выполнен
                    payment_update_dto.status_id = DbValueConstants.PaymentTransactionStatusRefundedID
                    payment_update_dto.rev_amount = refund_record.rev_amount
                    payment_update_dto.rev_desc = refund_record.rev_description
                    payment_update_dto.is_canceled = True
                    
                    await self.payment_transaction_repository.update(
                        obj=self.active_payment_transaction,
                        dto=payment_update_dto
                    )
                    
                    return (
                        DbValueConstants.TicketonOrderStatusCancelledRefundedID,
                        True,
                        "Возврат успешно выполнен банком"
                    )
                
                # ПРОБЛЕМЫ С ВОЗВРАТОМ
                elif refund_record.status in ("J", "F"):  # Rejected или Failed
                    payment_update_dto.status_id = DbValueConstants.PaymentTransactionStatusAwaitingRefundID
                    payment_update_dto.rev_amount = refund_record.rev_amount
                    payment_update_dto.rev_desc = refund_record.rev_description or "Возврат отклонен банком"
                    payment_update_dto.is_canceled = False
                    
                    await self.payment_transaction_repository.update(
                        obj=self.active_payment_transaction,
                        dto=payment_update_dto
                    )
                    
                    return (
                        DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                        False,
                        f"Возврат отклонен банком: {refund_record.rev_description or 'причина не указана'}"
                    )
                
                # ОЖИДАНИЕ ОБРАБОТКИ
                elif refund_record.status in ("r", "W", "w"):  # Waiting статусы
                    payment_update_dto.status_id = DbValueConstants.PaymentTransactionStatusAwaitingRefundID
                    payment_update_dto.rev_amount = refund_record.rev_amount
                    payment_update_dto.rev_desc = refund_record.rev_description or "Возврат в обработке банком"
                    
                    await self.payment_transaction_repository.update(
                        obj=self.active_payment_transaction,
                        dto=payment_update_dto
                    )
                    
                    return (
                        DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                        False,
                        "Возврат находится в обработке банком"
                    )
            
            # Нет подходящих записей возвратов
            return None
            
        except Exception as e:
            # Логируем ошибку, но не прерываем процесс
            # В реальном приложении здесь должно быть логирование
            return None
    
    def _create_safe_ticketon_update_dto(
        self, 
        status_id: int, 
        is_canceled: bool = True,
        cancel_reason: str | None = None
    ) -> TicketonOrderCDTO:
        """
        Безопасное создание DTO для обновления заказа Ticketon.
        
        Избегает проблем с SQLAlchemy lazy loading при обращении к relationship полям.
        
        Args:
            status_id: Новый статус заказа
            is_canceled: Флаг отмены заказа
            cancel_reason: Причина отмены (опционально)
            
        Returns:
            TicketonOrderCDTO: Готовый DTO для обновления
        """
        # Используем __dict__ для прямого доступа к колонкам без триггера relationships
        entity_dict = self.active_ticketon_order.__dict__
        
        return TicketonOrderCDTO(
            status_id=status_id,
            user_id=entity_dict.get('user_id'),
            payment_transaction_id=entity_dict.get('payment_transaction_id'),
            show=entity_dict.get('show'),
            show_info=entity_dict.get('show_info'),
            seats=entity_dict.get('seats'),
            lang=entity_dict.get('lang'),
            pre_sale=entity_dict.get('pre_sale'),
            sale=entity_dict.get('sale'),
            reservation_id=entity_dict.get('reservation_id'),
            price=entity_dict.get('price'),
            expire=entity_dict.get('expire'),
            expired_at=entity_dict.get('expired_at'),
            sum=entity_dict.get('sum'),
            currency=entity_dict.get('currency'),
            pre_tickets=entity_dict.get('pre_tickets'),
            tickets=entity_dict.get('tickets'),
            sale_secury_token=entity_dict.get('sale_secury_token'),
            is_active=entity_dict.get('is_active', False),
            is_paid=entity_dict.get('is_paid', False),
            is_canceled=is_canceled,
            cancel_reason=cancel_reason or entity_dict.get('cancel_reason'),
            email=entity_dict.get('email'),
            phone=entity_dict.get('phone')
        )
    
    def _create_safe_payment_transaction_update_dto(self) -> PaymentTransactionCDTO:
        """
        Безопасное создание DTO для обновления платежной транзакции.
        
        Избегает проблем с SQLAlchemy lazy loading при обращении к relationship полям.
        
        Returns:
            PaymentTransactionCDTO: Готовый DTO для обновления
        """
        # Используем __dict__ для прямого доступа к колонкам без триггера relationships
        entity_dict = self.active_payment_transaction.__dict__
        
        return PaymentTransactionCDTO(
            status_id=entity_dict.get('status_id'),
            user_id=entity_dict.get('user_id'),
            transaction_type=entity_dict.get('transaction_type'),
            order=entity_dict.get('order'),
            nonce=entity_dict.get('nonce'),
            mpi_order=entity_dict.get('mpi_order'),
            amount=entity_dict.get('amount'),
            currency=entity_dict.get('currency'),
            merchant=entity_dict.get('merchant'),
            language=entity_dict.get('language'),
            client_id=entity_dict.get('client_id'),
            desc=entity_dict.get('desc'),
            desc_order=entity_dict.get('desc_order'),
            email=entity_dict.get('email'),
            backref=entity_dict.get('backref'),
            wtype=entity_dict.get('wtype'),
            name=entity_dict.get('name'),
            pre_p_sign=entity_dict.get('pre_p_sign'),
            is_active=entity_dict.get('is_active', True),
            is_paid=entity_dict.get('is_paid', False),
            is_canceled=entity_dict.get('is_canceled', False),
            expired_at=entity_dict.get('expired_at'),
            res_code=entity_dict.get('res_code'),
            res_desc=entity_dict.get('res_desc'),
            paid_p_sign=entity_dict.get('paid_p_sign'),
            rev_amount=entity_dict.get('rev_amount'),
            rev_desc=entity_dict.get('rev_desc'),
            cancel_p_sign=entity_dict.get('cancel_p_sign'),
            order_full_info=entity_dict.get('order_full_info')
        )