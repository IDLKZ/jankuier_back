import traceback
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.cart.cart_action_dto import  CartActionResponseDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_and_payment_transaction.product_order_and_payment_transaction_repository import \
    ProductOrderAndPaymentTransactionRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.adapters.repository.product_order_item_history.product_order_item_history_repository import \
    ProductOrderItemHistoryRepository
from app.adapters.repository.product_order_item_status import ProductOrderItemStatusRepository
from app.adapters.repository.product_order_status import ProductOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderEntity, \
    ProductOrderItemEntity, PaymentTransactionEntity, ProductOrderAndPaymentTransactionEntity
from app.adapters.dto.product_order_response.product_order_response_dto import ProductOrderResponseDTO
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase
from app.use_case.cart.client.get_user_cart_case import GetUserCartCase


class RecreateProductOrderByIdCase(BaseUseCase[ProductOrderResponseDTO]):
    """
    Use Case для пересоздания платежной транзакции для существующего заказа на товары.

    Основная функциональность:
    - Валидирует существующий заказ пользователя
    - Деактивирует старые платежные транзакции
    - Создает новую платежную транзакцию с новым уникальным номером
    - Интегрируется с платежной системой Alatau
    - Устанавливает связь между заказом и новой транзакцией

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        product_order_item_repository: Репозиторий для работы с элементами заказа
        product_order_payment_transaction_repository: Репозиторий для связи заказ-платеж
        payment_transaction_repository: Репозиторий для платежных транзакций
        current_product_order: Существующий заказ для пересоздания
        current_product_order_items: Элементы заказа
        current_user: Текущий пользователь
        product_order_id: ID заказа для пересоздания
        order_dto: DTO для интеграции с платежной системой Alatau
        payment_transaction_entity: Созданная платежная транзакция
        response: Ответ с результатом пересоздания

    Raises:
        AppExceptionResponse: При ошибках валидации заказа или создания транзакции
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для пересоздания платежной транзакции заказа.

        Инициализирует все необходимые репозитории и instance переменные
        для работы с существующим заказом и создания новой платежной транзакции.

        Args:
            db: Активная сессия базы данных для выполнения операций

        Note:
            Все instance переменные инициализируются значениями по умолчанию
            и заполняются в процессе выполнения execute() метода.
        """

        # Инициализация репозиториев для работы с данными
        self.product_order_repository = ProductOrderRepository(db)
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.product_order_item_history_repository = ProductOrderItemHistoryRepository(db)
        self.product_order_status_repository = ProductOrderStatusRepository(db)
        self.product_order_item_status_repository = ProductOrderItemStatusRepository(db)
        self.product_order_payment_transaction_repository = ProductOrderAndPaymentTransactionRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.cart_repository = CartRepository(db)
        self.get_user_cart_use_case = GetUserCartCase(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.current_product_order: ProductOrderEntity | None = None  # Существующий заказ
        self.current_product_order_items: List[ProductOrderItemEntity] | None = None  # Элементы заказа

        # Входные данные для обработки
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь
        self.product_order_id: int | None = None  # ID заказа для пересоздания

        # Конфигурация заказа
        self.paid_at_minutes = 60 * 24  # Время для оплаты (24 часа)
        self.current_time = datetime.now()  # Текущее время создания заказа

        # Данные для платежной системы
        self.order_dto: AlatauCreateResponseOrderDTO | None = None  # DTO для платежной системы Alatau
        self.unique_order: str = "0000000000000000000000"  # Уникальный номер заказа
        # Результаты выполнения
        self.payment_transaction_entity: PaymentTransactionEntity | None = None  # Платежная транзакция
        self.response = ProductOrderResponseDTO(
            product_order=None,
            product_order_items=None,
            order=None,
            payment_transaction=None,
            is_success=False,
            message="OK"
        )

    async def execute(self, id: int, user: UserWithRelationsRDTO) -> ProductOrderResponseDTO:
        """
        Основной метод выполнения пересоздания платежной транзакции для заказа.

        Выполняет полный цикл пересоздания платежной транзакции:
        1. Валидирует существующий заказ пользователя
        2. Проверяет статус заказа и права доступа
        3. Деактивирует старые платежные транзакции
        4. Создает новую платежную транзакцию с уникальным номером
        5. Устанавливает связь между заказом и новой транзакцией

        Args:
            id (int): ID заказа для пересоздания платежной транзакции
            user (UserWithRelationsRDTO): Пользователь, запрашивающий пересоздание

        Returns:
            ProductOrderResponseDTO: Ответ содержащий:
                - product_order: Существующий заказ с relationships
                - product_order_items: Элементы заказа с relationships
                - order: DTO для новой платежной системы Alatau
                - payment_transaction: Созданная платежная транзакция
                - is_success: Флаг успешного выполнения
                - message: Сообщение об ошибке (если есть)

        Raises:
            AppExceptionResponse: При ошибках валидации заказа или создания транзакции
        """

        # Подготовка входных данных
        self.current_user = user
        self.product_order_id = id

        # Выполнение основной логики
        await self.validate()
        await self.transform()
        return self.response



    async def validate(self) -> None:
        """
        Валидация существующего заказа перед пересозданием платежной транзакции.

        Выполняет проверку готовности заказа к пересозданию платежной транзакции:
        1. Проверяет корректность входных параметров
        2. Загружает заказ по ID и проверяет принадлежность пользователю
        3. Проверяет статус заказа (должен ожидать оплаты)
        4. Загружает элементы заказа
        5. Заполняет response данными заказа

        Raises:
            AppExceptionResponse: С кодом bad_request если:
                - Заказ не найден (order not found)
                - Заказ не принадлежит пользователю
                - Заказ не активен, отменен или имеет неподходящий статус
                - Элементы заказа не найдены

        Note:
            Метод заполняет response объект данными заказа и элементов
            для возврата пользователю независимо от успеха операции.
        """
        if self.product_order_id is None or self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        self.current_product_order = await self.product_order_repository.get_first_with_filters(
            filters=[
                self.product_order_repository.model.id == self.product_order_id,
                self.product_order_repository.model.user_id == self.current_user.id
            ],
            options=self.product_order_repository.default_relationships()
        )
        if not self.current_product_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        if self.current_product_order.is_active is False or self.current_product_order.is_canceled is True or self.current_product_order.status_id not in [
            DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,#Ждем оплаты
        ]:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_is_not_active"))

        self.current_product_order_items = await self.product_order_item_repository.get_with_filters(
            filters=[
                self.product_order_item_repository.model.order_id == self.current_product_order.id
            ],
            options=self.product_order_item_repository.default_relationships()
        )

        if not self.current_product_order_items:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_items_not_found"))

        self.response.product_order = ProductOrderWithRelationsRDTO.model_validate(self.current_product_order)
        self.response.product_order_items = [ProductOrderItemWithRelationsRDTO.model_validate(item) for item in
                                             self.current_product_order_items]

    async def transform(self) -> None:
        """
        Основная бизнес-логика пересоздания платежной транзакции.

        Выполняет следующие операции в транзакционном режиме:
        1. Деактивирует все старые платежные транзакции для заказа
        2. Создает новую платежную транзакцию с новым уникальным номером
        3. Устанавливает связь между заказом и новой транзакцией

        Note:
            Метод не изменяет сам заказ, только создает новую возможность оплаты
            через новую платежную транзакцию с актуальными параметрами.
        """
        # Деактивация старых платежек
        await self._deactivate_old_transactions()
        # Создание новых платежек
        await self._create_new_transactions()




    async def _deactivate_old_transactions(self) -> None:
        """
        Деактивирует все существующие платежные транзакции для заказа.

        Находит все связи заказа с платежными транзакциями и:
        1. Деактивирует и отменяет сами платежные транзакции
        2. Деактивирует связи между заказом и транзакциями

        Note:
            Метод обеспечивает, что старые платежные ссылки становятся недействительными
            перед созданием новой транзакции.
        """
        # Деактивируем все платежки которые были инициированы ранее

        old_payment_transactions = await self.product_order_payment_transaction_repository.get_with_filters(
            filters=[
                self.product_order_payment_transaction_repository.model.product_order_id == self.current_product_order.id
            ],
            options=self.product_order_payment_transaction_repository.default_relationships()
        )
        # Находим и деактивируем платежки
        if old_payment_transactions:
            for payment_transaction_link in old_payment_transactions:
                if payment_transaction_link.payment_transaction:
                    # Деактивируем саму платежную транзакцию
                    transaction = payment_transaction_link.payment_transaction
                    transaction.is_active = False
                    transaction.is_canceled = True
                    transaction.is_paid = False

                    payment_transaction_dto = PaymentTransactionCDTO.model_validate(transaction)
                    await self.payment_transaction_repository.update(obj=transaction, dto=payment_transaction_dto)

            # Деактивируем связи между заказом и транзакциями
            await self.product_order_payment_transaction_repository.deactivate_links_for_order(
                product_order_id=self.product_order_id
            )


    async def _create_new_transactions(self) -> None:
        """
        Создает новую платежную транзакцию для заказа.

        Выполняет следующие операции:
        1. Генерирует новый уникальный номер заказа для платежной системы
        2. Создает DTO для интеграции с платежной системой Alatau
        3. Формирует цифровую подпись для безопасности
        4. Создает запись платежной транзакции в базе данных
        5. Устанавливает связь между заказом и новой транзакцией

        Note:
            Новая транзакция получает статус "ожидает оплаты" и срок действия
            на основе настроек существующего заказа.
        """
        # Генерируем уникальный номер заказа для платежной системы
        self.unique_order = await self.payment_transaction_repository.generate_unique_order(min_len=6, max_len=22)
        nonce = await self.payment_transaction_repository.generate_unique_noncense()
        user_name = f"{self.current_user.first_name or ''} {self.current_user.last_name or ''}".strip()

        # Создаем DTO для платежной системы Alatau
        self.order_dto = AlatauCreateResponseOrderDTO(
            ORDER=self.unique_order,
            AMOUNT=self.current_product_order.total_price,
            DESC="Покупка мерча",
            EMAIL=self.current_product_order.email,
            NONCE=nonce,
            CLIENT_ID=self.current_user.id,
            NAME=user_name,
            BACKREF=app_config.merch_backref
        )

        # Формируем цифровую подпись для безопасности
        self.order_dto.set_signature(app_config.shared_secret)

        # Создаем DTO для платежной транзакции
        payment_cdto = PaymentTransactionCDTO(
            user_id=self.current_user.id,
            status_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
            transaction_type=DbValueConstants.PaymentMerchType,
            order=self.unique_order,
            nonce=self.order_dto.NONCE,
            amount=self.current_product_order.total_price,
            currency="KZT",
            merchant=app_config.merchant_id,
            language="ru",
            client_id=self.current_user.id,
            desc="Покупка мерча",
            wtype=self.order_dto.WTYPE,
            backref=self.order_dto.BACKREF,
            email=self.current_product_order.email,
            name=self.order_dto.NAME if hasattr(self.order_dto, 'NAME') else None,
            pre_p_sign=self.order_dto.P_SIGN,
            is_active=True,
            is_paid=False,
            is_canceled=False,
            expired_at=self.current_product_order.paid_until
        )

        # Создаем запись платежной транзакции в базе данных
        self.payment_transaction_entity = await self.payment_transaction_repository.create(
            PaymentTransactionEntity(**payment_cdto.model_dump())
        )

        # 5. Создаем связь между заказом и платежной транзакцией
        await self.product_order_payment_transaction_repository.create(
            ProductOrderAndPaymentTransactionEntity(
                product_order_id=self.current_product_order.id,
                payment_transaction_id=self.payment_transaction_entity.id,
                link_type="recreated",  # Тип связи: пересозданная транзакция
                link_reason="Payment transaction recreated by user request",
                is_primary=True,  # Основная транзакция для заказа
                is_active=True
            )
        )

        # Заполняем успешный ответ
        self.response.order = self.order_dto
        self.response.payment_transaction = PaymentTransactionRDTO.model_validate(self.payment_transaction_entity)
        self.response.is_success = True



