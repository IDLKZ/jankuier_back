import datetime
import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefGetDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionWithRelationsRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderCDTO, ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO, ProductOrderItemCDTO
from app.adapters.dto.product_order_response.product_order_response_dto import \
    ProductOrderWithPaymentTransactionResponseDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_and_payment_transaction.product_order_and_payment_transaction_repository import \
    ProductOrderAndPaymentTransactionRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.adapters.repository.product_order_item_history import product_order_item_history_repository
from app.adapters.repository.product_order_item_history.product_order_item_history_repository import \
    ProductOrderItemHistoryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderEntity, PaymentTransactionEntity, ProductOrderItemHistoryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.firebase_service.firebase_service import FireBaseService
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class AcceptPaymentProductOrderCase(BaseUseCase[ProductOrderWithPaymentTransactionResponseDTO]):
    """
    Use Case для обработки подтверждения платежа заказов товаров через Alatau Pay.

    Основная функциональность:
    - Обрабатывает callback'и от платежной системы Alatau Pay после оплаты товаров
    - Валидирует цифровую подпись платежного запроса для обеспечения безопасности
    - Обновляет статус заказа товаров с "Ожидает оплаты" на "Оплачен"
    - Синхронизирует данные платежной транзакции с результатами от платежной системы
    - Автоматически активирует события на уровне Entity для обновления статусов элементов заказа
    - Возвращает полную информацию о заказе, элементах заказа и платежной транзакции

    Бизнес-логика:
    1. **Валидация callback'а**:
       - Проверка наличия данных в запросе
       - Верификация цифровой подписи с использованием shared_secret
       - Определение статуса оплаты по res_code ("0" = успешная оплата)
       - Поиск связанной платежной транзакции по order ID

    2. **Поиск и валидация заказа**:
       - Получение связи между платежной транзакцией и заказом товаров
       - Поиск заказа товаров и валидация его существования
       - Проверка статуса заказа (должен быть "Создан, ожидает оплаты")
       - Определение необходимости обновления данных

    3. **Обновление данных** (только при успешной оплате и корректном статусе):
       - Обновление PaymentTransactionEntity с данными от платежной системы
       - Деактивация платежной транзакции после обработки
       - При успешной оплате: обновление ProductOrderEntity со статусом "Оплачен"
       - Установка времени оплаты и связанных данных
       - Автоматическое срабатывание событий для обновления элементов заказа

    4. **Формирование ответа**:
       - Загрузка обновленного заказа с relationships
       - Получение всех элементов заказа с relationships
       - Формирование полного ответа с заказом, элементами и транзакцией

    Интеграция с событиями:
    - При обновлении ProductOrderEntity автоматически срабатывает ProductOrderEventHandler
    - Это приводит к синхронизации статусов элементов заказа согласно business rules
    - Статус "Оплачен" (ID=2) автоматически передается всем элементам заказа

    Архитектура:
    - **Repositories**: ProductOrderRepository, ProductOrderItemRepository, PaymentTransactionRepository, ProductOrderAndPaymentTransactionRepository
    - **Security**: Валидация цифровых подписей для защиты от подделки callback'ов
    - **Event Integration**: Автоматическая синхронизация через события Entity
    - **Error Handling**: Graceful обработка ошибок с детальными сообщениями

    Поддерживаемые типы запросов:
    - **AlatauBackrefGetDTO**: GET callback от Alatau Pay с результатами платежа

    Attributes:
        product_order_repository: Репозиторий для работы с заказами товаров
        product_order_item_repository: Репозиторий для работы с элементами заказов
        payment_transaction_repository: Репозиторий для работы с платежными транзакциями
        product_order_and_payment_transaction_repository: Репозиторий для связи заказов и транзакций
        current_product_order: Текущий обрабатываемый заказ товаров
        payment_transaction_entity: Платежная транзакция, связанная с заказом
        response: Объект ответа с полной информацией о результатах обработки
        dto: DTO с данными callback'а от платежной системы
        paid: Флаг успешности оплаты
        should_update: Флаг необходимости обновления данных

    Returns:
        ProductOrderWithPaymentTransactionResponseDTO: Содержит:
        - product_order: Заказ товаров с relationships
        - product_order_items: Список элементов заказа с relationships
        - payment_transaction: Платежная транзакция
        - is_success: Статус успешности оплаты
        - message: Сообщение о результате обработки

    Raises:
        AppExceptionResponse: При невалидной подписи, отсутствии транзакции или заказа

    Security Notes:
        - Все callback'и проверяются на валидность цифровой подписи
        - Используется shared_secret для верификации подлинности запросов
        - Обновление происходит только при корректном статусе заказа

    Flow Example:
        1. Пользователь оплачивает заказ товаров через Alatau Pay
        2. Alatau Pay отправляет callback с результатом оплаты
        3. AcceptPaymentProductOrderCase валидирует подпись и данные
        4. При успешной оплате обновляется статус заказа на "Оплачен"
        5. ProductOrderEventHandler автоматически обновляет элементы заказа
        6. Возвращается полная информация для уведомления пользователя
    """

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозиториев для работы с данными
        self.product_order_repository = ProductOrderRepository(db)
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.product_order_item_history_repository = ProductOrderItemHistoryRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.product_order_and_payment_transaction_repository = ProductOrderAndPaymentTransactionRepository(db)
        self.firebase_service = FireBaseService(db)

        self.current_product_order: ProductOrderEntity | None = None
        self.payment_transaction_entity: PaymentTransactionEntity | None = None  # Платежная транзакция

        self.response: ProductOrderWithPaymentTransactionResponseDTO = ProductOrderWithPaymentTransactionResponseDTO()
        self.dto: AlatauBackrefGetDTO|None = None
        self.paid: bool = False
        self.should_update: bool = False

    async def execute(self, dto: AlatauBackrefGetDTO) -> ProductOrderWithPaymentTransactionResponseDTO:
        # Подготовка входных данных
        self.dto = dto
        # Выполнение основной логики
        await self.validate()
        await self.transform()
        self.current_product_order = await self.product_order_repository.get_first_with_filters(
            filters=[self.product_order_repository.model.id == self.current_product_order.id],
            include_deleted_filter=True,
            options=self.product_order_repository.default_relationships()
        )
        self.current_product_order_items = await self.product_order_item_repository.get_with_filters(
            filters=[self.product_order_item_repository.model.order_id == self.current_product_order.id],
            include_deleted_filter=True,
            options=self.product_order_item_repository.default_relationships()
        )
        self.payment_transaction_entity = await self.payment_transaction_repository.get(
            id=self.payment_transaction_entity.id,
            options=self.payment_transaction_repository.default_relationships())
        self.response.product_order = ProductOrderWithRelationsRDTO.from_orm(self.current_product_order)
        self.response.product_order_items = [ProductOrderItemWithRelationsRDTO.from_orm(item) for item in self.current_product_order_items]
        self.response.payment_transaction = PaymentTransactionWithRelationsRDTO.from_orm(self.payment_transaction_entity)
        self.response.is_success = self.paid
        return self.response



    async def validate(self) -> None:
        if not self.dto:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("no_data"))
        if self.dto.verify_signature(app_config.shared_secret) is False:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("invalid_signature"))
        if self.dto.res_code == "0":
            self.paid = True
        self.payment_transaction_entity = await self.payment_transaction_repository.get_first_with_filters(
            filters=[self.payment_transaction_repository.model.order == self.dto.order],
            include_deleted_filter=True,
        )
        if not self.payment_transaction_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))

        payment_and_order = await self.product_order_and_payment_transaction_repository.get_first_with_filters(
            filters=[
                self.product_order_and_payment_transaction_repository.model.payment_transaction_id == self.payment_transaction_entity.id,
            ]
        )
        if not payment_and_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))
        self.current_product_order = await self.product_order_repository.get_first_with_filters(
            filters=[self.product_order_repository.model.id == payment_and_order.product_order_id],
            include_deleted_filter=True
        )
        if not self.current_product_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        if self.current_product_order.status_id == DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID:
            self.should_update = True


    async def transform(self) -> None:
        try:
            if self.should_update:
                #Если оплачен товар то можно обновить статус заказа продуктов
                payment_transaction_cdto = PaymentTransactionCDTO.from_orm(self.payment_transaction_entity)
                payment_transaction_cdto.mpi_order = self.dto.mpi_order
                payment_transaction_cdto.res_desc = self.dto.res_desc
                payment_transaction_cdto.res_code = self.dto.res_code
                payment_transaction_cdto.paid_p_sign = self.dto.sign
                payment_transaction_cdto.is_active = False
                payment_transaction_cdto.is_paid = self.paid
                if self.paid:
                    payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusPaidID
                else:
                    payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusFailedID
                self.payment_transaction_entity = await self.payment_transaction_repository.update(
                    obj=self.payment_transaction_entity,
                    dto=payment_transaction_cdto
                )
                if not self.payment_transaction_entity:
                    raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_updated"))
                if self.paid:
                    product_order_cdto = ProductOrderCDTO.from_orm(self.current_product_order)
                    product_order_cdto.status_id = DbValueConstants.ProductOrderStatusPaidID
                    product_order_cdto.payment_transaction_id = self.payment_transaction_entity.id
                    product_order_cdto.paid_order = self.dto.order
                    product_order_cdto.is_paid = self.paid
                    product_order_cdto.paid_at = datetime.datetime.now()
                    self.current_product_order = await self.product_order_repository.update(
                        obj=self.current_product_order,
                        dto=product_order_cdto
                    )
                    await self.firebase_service.send_payment_product_successfull_notification(self.current_product_order.user_id, self.current_product_order)

                    # Обновляем is_paid = True для всех элементов заказа при успешной оплате
                    order_items = await self.product_order_item_repository.get_with_filters(
                        filters=[self.product_order_item_repository.model.order_id == self.current_product_order.id],
                        include_deleted_filter=True
                    )
                    for item in order_items:
                        item_cdto = ProductOrderItemCDTO.from_orm(item)
                        item_cdto.is_paid = True
                        product_item_updated = await self.product_order_item_repository.update(
                            obj=item,
                            dto=item_cdto
                        )
                        # if product_item_updated :
                        #     await self.product_order_item_history_repository.create(
                        #         obj=ProductOrderItemHistoryEntity(
                        #             order_item_id=product_item_updated.id,
                        #             status_id=DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID
                        #     ))



                self.response.message = "OK"
        except Exception as exc:
            self.response.message = traceback.print_exc()









