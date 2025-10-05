import traceback
from typing import Union, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import dto
from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefResponseDTO, AlatauBackrefGetDTO, \
    AlatauBackrefPostDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, \
    PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_confirm_sale_dto import TicketonConfirmSaleRequestDTO, \
    TicketonConfirmSaleResponseDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderCDTO, TicketonOrderWithRelationsRDTO, \
    TicketonOrderRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.adapters.repository.ticketon_order_and_payment_transaction.ticketon_order_and_payment_transaction_repository import \
    TicketonOrderAndPaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity, PaymentTransactionEntity, TicketonOrderAndPaymentTransactionEntity
from app.helpers.alatau_helper import get_alatau_error_message
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.firebase_service.firebase_service import FireBaseService
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase, T


class TicketonConfirmCase(BaseUseCase[AlatauBackrefResponseDTO]):
    """
    Use Case для обработки подтверждения платежа заказов Ticketon через Alatau Pay.

    Основная функциональность:
    - Обрабатывает callback'и от платежной системы Alatau Pay после оплаты билетов Ticketon
    - Валидирует цифровую подпись платежного запроса для обеспечения безопасности
    - Обновляет статус платежной транзакции в зависимости от результата оплаты
    - При успешной оплате подтверждает заказ билетов в системе Ticketon
    - Синхронизирует данные между локальной БД и внешним API Ticketon
    - Возвращает полную информацию о заказе и транзакции для дальнейшей обработки

    Бизнес-логика:
    1. **Валидация запроса**:
       - Проверка обязательных полей (order, sign)
       - Верификация цифровой подписи с использованием shared_secret
       - Поиск и валидация связанной платежной транзакции
       - Проверка активности заказа Ticketon

    2. **Обработка платежа**:
       - Определение статуса оплаты по res_code ("0" = успех)
       - Обновление PaymentTransactionEntity с результатами платежа
       - Сохранение данных о транзакции (amount, currency, mpi_order, etc.)
       - Деактивация платежной транзакции после обработки

    3. **Подтверждение в Ticketon** (только при успешной оплате):
       - Вызов API Ticketon для подтверждения продажи билетов
       - Обновление TicketonOrderEntity с данными подтвержденного заказа
       - Сохранение информации о билетах и деталях заказа
       - Установка соответствующего статуса заказа

    Архитектура:
    - **Repositories**: TicketonOrderRepository, PaymentTransactionRepository, TicketonOrderAndPaymentTransactionRepository
    - **External Services**: TicketonServiceAPI для взаимодействия с внешним API
    - **Security**: Валидация цифровых подписей для защиты от подделки запросов
    - **Error Handling**: Обработка ошибок API Ticketon и внутренних сбоев

    Поддерживаемые типы запросов:
    - **AlatauBackrefPostDTO**: POST callback от Alatau Pay
    - **AlatauBackrefGetDTO**: GET callback от Alatau Pay

    Attributes:
        ticketon_order_repository: Репозиторий для работы с заказами Ticketon
        payment_transaction_repository: Репозиторий для работы с платежными транзакциями
        ticketon_order_and_payment_transaction_repository: Репозиторий для связи заказов и транзакций
        ticketon_service_api: Сервис для взаимодействия с API Ticketon
        dto: DTO с данными callback'а от платежной системы
        ticketon_order_entity: Экземпляр заказа Ticketon
        payment_transaction_entity: Экземпляр платежной транзакции
        response: Объект ответа с результатами обработки

    Returns:
        AlatauBackrefResponseDTO: Содержит информацию о заказе, транзакции, статусе и сообщениях

    Raises:
        AppExceptionResponse: При невалидной подписи, отсутствии транзакции, неактивном заказе

    Security Notes:
        - Все callback'и проверяются на валидность цифровой подписи
        - Используется shared_secret для верификации подлинности запросов
        - Транзакции проверяются на активность перед обработкой

    Integration Points:
        - **Alatau Pay**: Получение callback'ов о статусе платежа
        - **Ticketon API**: Подтверждение заказов и получение билетов
        - **Local Database**: Обновление статусов заказов и транзакций
    """

    def __init__(self, db: AsyncSession) -> None:
        #Repositories
        self.ticketon_order_repository = TicketonOrderRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.ticketon_order_and_payment_transaction_repository = TicketonOrderAndPaymentTransactionRepository(db)
        self.firebase_service = FireBaseService(db)
        #Services
        self.ticketon_service_api = TicketonServiceAPI()
        #DTO
        self.dto:Union[AlatauBackrefPostDTO|AlatauBackrefGetDTO|None] = None
        self.ticketon_order_entity: TicketonOrderEntity | None = None
        self.payment_transaction_entity: PaymentTransactionEntity | None = None
        self.response = AlatauBackrefResponseDTO()
        self.ticketon_order_and_payment_transaction_entity:TicketonOrderAndPaymentTransactionEntity|None = None

    async def execute(self, dto:Union[AlatauBackrefPostDTO|AlatauBackrefGetDTO]) -> AlatauBackrefResponseDTO:
        self.dto = dto
        await self.validate()
        await self.transform()
        return self.response



    async def validate(self) -> None:
        # Проверяем обязательные поля
        if not self.dto.order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("order_is_required"))
        if not self.dto.sign:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("signature_is_required"))

        #Проверим подпись
        if isinstance(self.dto, AlatauBackrefPostDTO):
            if not self.dto.verify_signature(shared_key=app_config.shared_secret):
                raise AppExceptionResponse.bad_request(message=i18n.gettext("invalid_signature"))
        if isinstance(self.dto, AlatauBackrefGetDTO):
            if not self.dto.verify_signature(shared_key=app_config.shared_secret):
                raise AppExceptionResponse.bad_request(message=i18n.gettext("invalid_signature"))
        #Проверяем транзакцию
        self.payment_transaction_entity = await self.payment_transaction_repository.get_first_with_filters(
            filters=[
                self.payment_transaction_repository.model.order == self.dto.order,
                self.payment_transaction_repository.model.transaction_type == DbValueConstants.PaymentTicketonType
            ],
            include_deleted_filter=True
        )
        if self.payment_transaction_entity is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))

        if self.payment_transaction_entity.is_active is False or self.payment_transaction_entity.is_canceled is True:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_is_not_active"))

        self.ticketon_order_and_payment_transaction_entity = await self.ticketon_order_and_payment_transaction_repository.get_first_with_filters(
            filters=[
                self.ticketon_order_and_payment_transaction_repository.model.payment_transaction_id == self.payment_transaction_entity.id,
                self.ticketon_order_and_payment_transaction_repository.model.is_active.is_(True)
            ]
        )
        if not self.ticketon_order_and_payment_transaction_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_and_payment_transaction_not_found"))
        #Проверяем заказ
        self.ticketon_order_entity = await self.ticketon_order_repository.get_first_with_filters(
            filters=[
                self.ticketon_order_repository.model.id == self.ticketon_order_and_payment_transaction_entity.ticketon_order_id
            ],
            options=self.ticketon_order_repository.default_relationships(),
            include_deleted_filter=True
        )
        if self.ticketon_order_entity is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_not_found"))
        if self.ticketon_order_entity.is_active is False or self.ticketon_order_entity.is_canceled is True:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_not_active"))


    async def transform(self):
        is_paid = False
        payment_status_id = DbValueConstants.PaymentTransactionStatusFailedID
        error_message:str|None = None

        if self.dto.res_code == "0":
            is_paid = True
            payment_status_id = DbValueConstants.PaymentTransactionStatusPaidID

        payment_transaction_cdto = PaymentTransactionCDTO.from_orm(self.payment_transaction_entity)
        payment_transaction_cdto.mpi_order = getattr(self.dto, 'mpi_order', self.dto.order) or self.dto.order
        payment_transaction_cdto.status_id = payment_status_id
        payment_transaction_cdto.amount = float(self.dto.amount) if self.dto.amount else 0.0
        payment_transaction_cdto.currency = self.dto.currency or ""
        payment_transaction_cdto.paid_p_sign = self.dto.sign or ""
        payment_transaction_cdto.is_paid = is_paid
        payment_transaction_cdto.is_active = False
        payment_transaction_cdto.is_canceled = False
        if isinstance(self.dto, AlatauBackrefPostDTO):
            payment_transaction_cdto.res_code = self.dto.rc
            if self.dto.rc != "00":
                payment_transaction_cdto.res_desc = get_alatau_error_message(int(self.dto.rc),"ru")
        if isinstance(self.dto, AlatauBackrefGetDTO):
            payment_transaction_cdto.res_code = self.dto.res_code
            payment_transaction_cdto.res_desc = self.dto.res_desc
        new_pt = await self.payment_transaction_repository.update(obj=self.payment_transaction_entity,
                                                                  dto=payment_transaction_cdto)
        if new_pt is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_updated"))

        self.payment_transaction_entity = await self.payment_transaction_repository.get_first_with_filters(
            filters=[
                self.payment_transaction_repository.model.id == new_pt.id,
            ],
            options=self.payment_transaction_repository.default_relationships(),
            include_deleted_filter=True
        )
        error_message = self.payment_transaction_entity.res_desc

        if is_paid:
            try:
                ticketon_confirm_request = TicketonConfirmSaleRequestDTO(
                    sale=self.ticketon_order_entity.sale,
                    email=self.ticketon_order_entity.email,
                    phone=self.ticketon_order_entity.phone
                )
                ticketon_confirm_response:TicketonConfirmSaleResponseDTO = await self.ticketon_service_api.sale_confirm(dto=ticketon_confirm_request)
                ticketon_udto = TicketonOrderCDTO.from_orm(self.ticketon_order_entity)
                ticketon_udto.sale = ticketon_confirm_response.sale
                ticketon_udto.price = ticketon_confirm_response.price
                ticketon_udto.expire = ticketon_confirm_response.expire
                ticketon_udto.sum = ticketon_confirm_response.sum
                ticketon_udto.show = ticketon_confirm_response.show
                ticketon_udto.is_active = False
                ticketon_udto.is_paid = True
                ticketon_udto.payment_transaction_id = self.payment_transaction_entity.id
                ticketon_udto.tickets = [ticket.model_dump() if hasattr(ticket, 'model_dump') else ticket for ticket in ticketon_confirm_response.tickets] if ticketon_confirm_response.tickets else None
                if ticketon_confirm_response.status == 1:
                    ticketon_udto.status_id = DbValueConstants.TicketonOrderStatusPaidConfirmedID
                else:
                    ticketon_udto.status_id = DbValueConstants.TicketonOrderStatusPaidAwaitingConfirmationID
                updated_ticketon_order_entity = await self.ticketon_order_repository.update(obj=self.ticketon_order_entity, dto=ticketon_udto)
                self.ticketon_order_entity = await self.ticketon_order_repository.get_first_with_filters(
                    filters=[
                        self.ticketon_order_repository.model.id == updated_ticketon_order_entity.id
                    ],
                    options=self.ticketon_order_repository.default_relationships(),
                    include_deleted_filter=True,
                )
                await self.firebase_service.send_ticketon_notification(user_id=self.ticketon_order_entity.user_id, ticketon=self.ticketon_order_entity)
            except Exception as e:
                error_message = str(e)

        # Ensure relationships are loaded for final response
        if not is_paid or self.ticketon_order_entity is None:
            self.ticketon_order_entity = await self.ticketon_order_repository.get_first_with_filters(
                filters=[
                    self.ticketon_order_repository.model.id == self.ticketon_order_and_payment_transaction_entity.ticketon_order_id
                ],
                options=self.ticketon_order_repository.default_relationships(),
                include_deleted_filter=True,
            )
        try:

            self.response.ticketon_order = TicketonOrderWithRelationsRDTO.model_validate(self.ticketon_order_entity)
            self.response.payment_transaction = PaymentTransactionWithRelationsRDTO.model_validate(self.payment_transaction_entity)
            self.response.status = is_paid
            self.response.message = error_message


        except Exception as e:

            details = traceback.format_exc()

            raise AppExceptionResponse.internal_error(

                message=i18n.gettext("internal_server_error"),

                extra={"details": details}

            )








