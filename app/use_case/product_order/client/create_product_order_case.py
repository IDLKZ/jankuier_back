import traceback
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from sqlalchemy import func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.cart.cart_action_dto import  CartActionResponseDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
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


class CreateProductOrderCase(BaseUseCase[ProductOrderResponseDTO]):
    """
    Use Case для создания заказа на товары из корзины пользователя.

    Основная функциональность:
    - Валидирует корзину пользователя и её содержимое
    - Создает заказ (ProductOrder) на основе данных корзины
    - Создает элементы заказа (ProductOrderItem) для каждого товара
    - Генерирует платежную транзакцию и интегрируется с платежной системой Alatau
    - Устанавливает связь между заказом и платежной транзакцией
    - Удаляет корзину после успешного создания заказа
    - Обрабатывает ошибки с откатом транзакций

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        product_order_item_repository: Репозиторий для работы с элементами заказа
        product_order_item_history_repository: Репозиторий для истории элементов заказа
        product_order_status_repository: Репозиторий для статусов заказа
        product_order_item_status_repository: Репозиторий для статусов элементов заказа
        product_order_payment_transaction_repository: Репозиторий для связи заказ-платеж
        payment_transaction_repository: Репозиторий для платежных транзакций
        cart_repository: Репозиторий для корзин
        get_user_cart_use_case: Use Case для получения корзины пользователя
        current_product_order: Созданный заказ
        current_product_order_item: Элементы созданного заказа
        current_user: Текущий пользователь
        data: Данные корзины пользователя
        order_dto: DTO для интеграции с платежной системой Alatau
        payment_transaction_entity: Созданная платежная транзакция
        response: Ответ с результатом создания заказа

    Raises:
        AppExceptionResponse: При ошибках валидации, создания заказа или платежной транзакции
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для создания заказа.

        Инициализирует все необходимые репозитории и instance переменные
        для создания заказа, элементов заказа и платежной транзакции.

        Args:
            db: Активная сессия базы данных для выполнения операций

        Note:
            Все instance переменные инициализируются значениями по умолчанию
            и заполняются в процессе выполнения execute() метода.
            Время оплаты заказа по умолчанию установлено на 24 часа (1440 минут).
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
        self.current_product_order: ProductOrderEntity | None = None  # Созданный заказ
        self.current_product_order_item: List[ProductOrderItemEntity] | None = None  # Элементы заказа

        # Входные данные для обработки
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь
        self.data: CartActionResponseDTO | None = None  # Данные корзины пользователя

        # Конфигурация заказа
        self.paid_at_minutes = 60 * 24  # Время для оплаты (24 часа)
        self.current_time = datetime.now()  # Текущее время создания заказа

        # Данные для платежной системы
        self.order_dto = AlatauCreateResponseOrderDTO()  # DTO для платежной системы Alatau
        self.unique_order: str = "0000000000000000000000"  # Уникальный номер заказа
        self.phone: str = ""  # Телефон для заказа
        self.email: str = ""  # Email для заказа

        # Результаты выполнения
        self.payment_transaction_entity: PaymentTransactionEntity | None = None  # Платежная транзакция
        self.response: ProductOrderResponseDTO = ProductOrderResponseDTO()  # Ответ use case

    async def execute(self, user: UserWithRelationsRDTO, phone: str | None = None, email: str | None = None) -> ProductOrderResponseDTO:
        """
        Основной метод выполнения создания заказа из корзины пользователя.

        Выполняет полный цикл создания заказа:
        1. Подготавливает входные данные (пользователь, телефон, email)
        2. Валидирует корзину пользователя и её содержимое
        3. Создает заказ, элементы заказа и платежную транзакцию
        4. Загружает созданные данные с relationships
        5. Формирует и возвращает ответ

        Args:
            user (UserWithRelationsRDTO): Пользователь создающий заказ
            phone (str | None, optional): Телефон для заказа.
                Если не указан, используется телефон из профиля пользователя
            email (str | None, optional): Email для заказа.
                Если не указан, используется email из профиля пользователя

        Returns:
            ProductOrderResponseDTO: Ответ содержащий:
                - product_order: Созданный заказ с relationships
                - product_order_items: Элементы заказа с relationships
                - order: DTO для платежной системы Alatau
                - payment_transaction: Созданная платежная транзакция
                - is_success: Флаг успешного выполнения
                - message: Сообщение об ошибке (если есть)

        Raises:
            AppExceptionResponse: При ошибках валидации корзины или создания заказа
        """
        # Подготовка входных данных
        self.current_user = user
        self.phone = (phone if phone is not None else user.phone)
        self.email = (email if email is not None else user.email)

        # Выполнение основной логики
        await self.validate()
        await self.transform()

        # Загрузка созданных данных с relationships для ответа
        self.current_product_order = await self.product_order_repository.get(
            self.current_product_order.id,
            options=self.product_order_repository.default_relationships()
        )
        self.current_product_order_item = await self.product_order_item_repository.get_with_filters(
            filters=[self.product_order_item_repository.model.order_id == self.current_product_order.id],
            options=self.product_order_item_repository.default_relationships()
        )

        # Формирование ответа
        self.response.product_order = ProductOrderWithRelationsRDTO.from_orm(self.current_product_order)
        self.response.product_order_items = [ProductOrderWithRelationsRDTO.from_orm(item) for item in self.current_product_order_item]

        return self.response


    async def validate(self) -> None:
        """
        Валидация корзины пользователя перед созданием заказа.

        Выполняет проверку готовности корзины к оформлению заказа:
        1. Загружает корзину пользователя через GetUserCartCase
        2. Проверяет наличие корзины
        3. Проверяет наличие элементов в корзине
        4. Проверяет корректность пользователя
        5. Проверяет что общая стоимость больше нуля

        Raises:
            AppExceptionResponse: С кодом bad_request если:
                - Корзина не найдена (cart is None)
                - Корзина пустая (cart_items is None or empty)
                - Пользователь не указан (current_user is None)
                - Общая стоимость корзины <= 0

        Note:
            Метод заполняет self.data объектом CartActionResponseDTO
            для использования в transform() методе.
        """
        # Получаем корзину пользователя
        self.data = await self.get_user_cart_use_case.execute(user=self.current_user)

        # Проверяем готовность корзины к оформлению заказа
        if (self.data.cart is None or
            self.data.cart_items is None or
            self.current_user is None or
            self.data.total_price <= 0):
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_is_not_ready"))

    async def transform(self) -> None:
        """
        Основная бизнес-логика создания заказа, элементов заказа и платежной транзакции.

        Выполняет следующие операции в транзакционном режиме:

        1. **Создание заказа (ProductOrder)**:
           - Создает заказ со статусом "Создан, ожидает оплаты"
           - Устанавливает срок оплаты (по умолчанию 24 часа)
           - Сохраняет снапшот корзины в поле order_items

        2. **Создание элементов заказа (ProductOrderItem)**:
           - Для каждого элемента корзины создает соответствующий элемент заказа
           - Устанавливает статус "Создан, ожидает оплаты"
           - Копирует все данные о товаре, цене, количестве

        3. **Удаление корзины**:
           - После успешного создания заказа удаляет корзину пользователя
           - Использует force_delete для полного удаления

        4. **Создание платежной транзакции**:
           - Генерирует уникальный номер заказа для платежной системы
           - Создает DTO для интеграции с платежной системой Alatau
           - Формирует цифровую подпись для безопасности
           - Создает запись платежной транзакции

        5. **Связывание заказа с платежом**:
           - Создает связь между заказом и платежной транзакцией
           - Устанавливает тип связи "initial" (первоначальная)

        Raises:
            AppExceptionResponse: При ошибках создания заказа или элементов заказа.
                В случае ошибки выполняется откат с удалением созданного заказа.

        Note:
            Метод использует try-catch блоки для обеспечения целостности данных.
            При любой ошибке в создании элементов заказа, созданный заказ удаляется.
            Ошибки в создании платежной транзакции обрабатываются мягко и записываются
            в response.message без прерывания выполнения.

        Warning:
            Метод изменяет состояние response объекта, устанавливая:
            - order: DTO для платежной системы
            - payment_transaction: Созданная транзакция
            - is_success: Флаг успешного выполнения
            - message: Сообщение об ошибке (если есть)
        """
        # 1. Создаем основной заказ (ProductOrder)
        try:
            self.current_product_order = await self.product_order_repository.create(
                ProductOrderEntity(
                    user_id=self.current_user.id,
                    status_id=DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,
                    total_price=self.data.total_price,
                    order_items=self.data.cart_items,  # Снапшот корзины для истории
                    email=self.email,
                    phone=self.phone,
                    paid_until=self.current_time + timedelta(minutes=self.paid_at_minutes)
                ))
        except AppExceptionResponse as e:
            # Откат: удаляем созданный заказ при ошибке
            if self.current_product_order:
                await self.product_order_repository.delete(self.current_product_order.id, force_delete=True)
            raise e

        # Проверяем что заказ успешно создан
        if not self.current_product_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("order_not_formed"))

        # 2. Создаем элементы заказа (ProductOrderItem) для каждого товара в корзине
        try:
            product_order_items = []
            # Создаем элемент заказа для каждого товара в корзине
            for item in self.data.cart_items:
                product_order_item = await self.product_order_item_repository.create(
                    ProductOrderItemEntity(
                        order_id=self.current_product_order.id,
                        status_id=DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,
                        product_id=item.product_id,
                        variant_id=item.variant_id,
                        from_city_id=item.from_city_id,
                        # to_city_id=user.city_id,
                        qty=item.qty,
                        sku=item.sku,
                        product_price=item.product_price,
                        delta_price=item.delta_price,
                    )
                )
                product_order_items.append(product_order_item)
        except AppExceptionResponse as e:
            # Откат: удаляем заказ если не удалось создать элементы
            if self.current_product_order:
                await self.product_order_repository.delete(self.current_product_order.id, force_delete=True)
            raise e

        # 3. Удаляем корзину после успешного создания заказа
        if self.current_product_order and product_order_items:
            await self.cart_repository.delete(self.data.cart.id, force_delete=True)

        # 4. Создаем платежную транзакцию и интеграцию с платежной системой Alatau
        try:
            # Генерируем уникальный номер заказа для платежной системы
            self.unique_order = await self.payment_transaction_repository.generate_unique_order(min_len=6, max_len=22)

            # Заполняем DTO для платежной системы Alatau
            self.order_dto.ORDER = self.unique_order
            self.order_dto.AMOUNT = self.data.total_price
            self.order_dto.DESC = "Покупка мерча"
            self.order_dto.EMAIL = self.email
            self.order_dto.PHONE = self.phone
            self.order_dto.NONCE = await self.payment_transaction_repository.generate_unique_noncense()
            self.order_dto.CLIENT_ID = self.current_user.id
            self.order_dto.NAME = f"{self.current_user.first_name or ''} {self.current_user.last_name or ''}".strip()

            # Формируем цифровую подпись для безопасности
            self.order_dto.set_signature(app_config.shared_secret)

            # Создаем DTO для платежной транзакции
            payment_cdto = PaymentTransactionCDTO(
                user_id=self.current_user.id,
                status_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                transaction_type=DbValueConstants.PaymentMerchType,
                order=self.unique_order,
                nonce=self.order_dto.NONCE,
                amount=self.data.total_price,
                currency="KZT",
                merchant=app_config.merchant_id,
                language="ru",
                client_id=self.current_user.id,
                desc="Покупка мерча",
                email=self.email,
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
                    link_type="initial",  # Тип связи: первоначальная транзакция
                    link_reason="Initial order creation",
                    is_primary=True,  # Основная транзакция для заказа
                    is_active=True
                )
            )

            # Заполняем успешный ответ
            self.response.order = self.order_dto
            self.response.payment_transaction = PaymentTransactionRDTO.model_validate(self.payment_transaction_entity)
            self.response.is_success = True

        except Exception as e:
            # Мягкая обработка ошибок платежной системы (не прерываем процесс)
            self.response.is_success = False
            self.response.message = traceback.format_exc()
            # Продолжаем выполнение, заказ уже создан


