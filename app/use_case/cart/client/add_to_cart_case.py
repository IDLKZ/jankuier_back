"""
Use Case для добавления товаров в корзину покупателя.

Модуль содержит реализацию бизнес-логики добавления товаров в корзину,
включая валидацию доступности товаров, работу с вариантами товаров,
проверку stock и автоматический расчет цен.

Classes:
    AddToCartCase: Use Case для добавления товара в корзину пользователя

Dependencies:
    - CartRepository: Для работы с корзинами
    - CartItemRepository: Для работы с элементами корзины
    - ProductRepository: Для работы с товарами
    - ProductVariantRepository: Для работы с вариантами товаров

Author: Claude Code Assistant
"""

from decimal import Decimal
from typing import List

from sqlalchemy import func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_action_dto import AddToCartDTO, CartActionResponseDTO
from app.adapters.dto.cart.cart_dto import CartRDTO, CartWithRelationsRDTO
from app.adapters.dto.cart_item.cart_item_dto import CartItemCDTO, CartItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity, ProductVariantEntity, ProductEntity, CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class AddToCartCase(BaseUseCase[CartActionResponseDTO]):
    """
    Use Case для добавления товара в корзину пользователя.

    Основная функциональность:
    - Создает корзину пользователя если её ещё нет
    - Проверяет доступность товара и его варианта (если указан)
    - Увеличивает количество если товар уже есть в корзине
    - Создает новый элемент корзины если товара в корзине нет
    - Валидирует stock перед добавлением и обновлением
    - Автоматически рассчитывает цены с учетом вариантов

    Attributes:
        cart_repository: Репозиторий для работы с корзинами
        cart_item_repository: Репозиторий для работы с элементами корзины
        product_repository: Репозиторий для работы с товарами
        product_item_repository: Репозиторий для работы с вариантами товаров
        cart_entity: Корзина пользователя (инициализируется в процессе выполнения)
        cart_item_entity: Существующий элемент корзины (если товар уже есть)
        cart_items_entity: Все элементы корзины пользователя
        current_product: Товар который добавляется в корзину
        current_product_variant_entity: Вариант товара (если указан)
        dto: Входные данные для добавления товара
        current_user: Текущий пользователь

    Raises:
        AppExceptionResponse: При ошибках валидации, отсутствии товара или недостатке stock
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для добавления товара в корзину.

        Инициализирует все необходимые репозитории и instance переменные
        для хранения состояния во время выполнения операции.

        Args:
            db: Активная сессия базы данных для выполнения операций

        Note:
            Все instance переменные инициализируются значениями по умолчанию
            и заполняются в процессе выполнения execute() метода.
        """
        # Инициализация репозиториев для работы с данными
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
        self.product_item_repository = ProductVariantRepository(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.cart_entity: CartEntity | None = None  # Корзина пользователя
        self.cart_item_entity: CartItemEntity | None = None  # Существующий элемент корзины (если есть)
        self.cart_items_entity: List[CartItemEntity] | None = []  # Все элементы корзины пользователя
        self.current_product: ProductEntity | None = None  # Добавляемый товар
        self.current_product_variant_entity: ProductVariantEntity | None = None  # Вариант товара (если есть)

        # Входные данные для обработки
        self.dto: AddToCartDTO | None = None  # DTO с данными о добавляемом товаре
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь

    async def execute(self, dto: AddToCartDTO, user: UserWithRelationsRDTO) -> CartActionResponseDTO:
        """
        Основной метод выполнения добавления товара в корзину.

        Выполняет полный цикл добавления товара в корзину:
        1. Валидирует входные данные и доступность товара
        2. Создает корзину пользователя если её нет
        3. Добавляет товар в корзину или увеличивает количество
        4. Возвращает актуальное состояние корзины

        Args:
            dto (AddToCartDTO): DTO с данными о добавляемом товаре.
                Содержит product_id, variant_id (опционально) и qty
            user (UserWithRelationsRDTO): Текущий пользователь с загруженными relationships

        Returns:
            CartActionResponseDTO: Ответ содержащий:
                - cart: Обновленная корзина пользователя
                - cart_items: Все элементы корзины с relationships
                - total_price: Рассчитанная общая стоимость корзины

        Raises:
            AppExceptionResponse: При ошибках валидации, недоступности товара,
                                недостатке stock или других бизнес-ошибках

        Example:
            >>> dto = AddToCartDTO(product_id=1, variant_id=2, qty=3)
            >>> result = await case.execute(dto, user)
            >>> print(f"Total: {result.total_price}")
        """
        # Сохраняем входные данные в instance переменные
        self.dto = dto
        self.current_user = user

        # Валидируем входные данные и доступность товара
        await self.validate()

        # Выполняем бизнес-логику добавления в корзину
        await self.transform()

        # Получаем обновленную корзину с relationships для возврата
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id],
            options=self.cart_repository.default_relationships()
        )
        if self.cart_entity:
            self.cart_items_entity = await self.cart_item_repository.get_with_filters(
                filters=[self.cart_item_repository.model.cart_id == self.cart_entity.id],
                options=self.cart_item_repository.default_relationships()
            )

        # Вычисляем общую стоимость корзины вручную
        calculated_total_price = 0.0
        cart_items_dto = []
        if self.cart_items_entity:
            for cart_item in self.cart_items_entity:
                cart_items_dto.append(CartItemWithRelationsRDTO.from_orm(cart_item))
                calculated_total_price += float(cart_item.total_price)

        # Формируем ответ с актуальными данными и рассчитанной общей стоимостью
        return CartActionResponseDTO(
            cart=CartWithRelationsRDTO.from_orm(self.cart_entity),
            cart_items=cart_items_dto,
            total_price=calculated_total_price,
        )

    async def validate(self) -> None:
        """
        Валидация входных данных и доступности товара.

        Выполняет комплексную проверку всех данных необходимых для добавления товара:
        1. Проверяет наличие обязательных параметров (dto и user)
        2. Загружает и проверяет существование товара по product_id
        3. Валидирует доступность товара (is_active=True, stock > 0)
        4. Проверяет достаточность stock для запрашиваемого количества
        5. Если указан variant_id:
           - Загружает вариант товара и проверяет его принадлежность товару
           - Валидирует доступность варианта (is_active=True, stock > 0)
           - Проверяет достаточность stock варианта

        Raises:
            AppExceptionResponse: При любой ошибке валидации:
                - bad_request: Если отсутствуют dto или user
                - bad_request: Если товар не найден или недоступен
                - bad_request: Если вариант не найден или недоступен
                - bad_request: Если недостаточно stock

        Note:
            Метод заполняет self.current_product и self.current_product_variant_entity
            для использования в transform() методе.
        """
        # Проверяем наличие обязательных параметров
        if self.dto is None or self.current_user is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("user_or_dto_not_included"))

        # Получаем и проверяем существование товара
        self.current_product = await self.product_repository.get(self.dto.product_id)
        if not self.current_product:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_not_found"))

        # Проверяем доступность товара и достаточность stock
        if (self.current_product.is_active is False or
            self.current_product.stock <= 0 or
            self.dto.qty > self.current_product.stock):
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_not_available"))

        # Если указан variant_id, проверяем вариант товара
        if self.dto.variant_id:
            # Получаем вариант товара, который принадлежит указанному продукту
            self.current_product_variant_entity = await self.product_item_repository.get_first_with_filters(
                filters=[
                    and_(
                        self.product_item_repository.model.product_id == self.current_product.id,
                        self.product_item_repository.model.id == self.dto.variant_id
                    )
                ]
            )
            if not self.current_product_variant_entity:
                raise AppExceptionResponse.bad_request(message=i18n.gettext("product_variant_not_found"))

            # Проверяем доступность варианта и достаточность stock
            if (self.current_product_variant_entity.is_active is False or
                self.current_product_variant_entity.stock <= 0 or
                self.dto.qty > self.current_product_variant_entity.stock):
                raise AppExceptionResponse.bad_request(message=i18n.gettext("product_variant_not_available"))

    async def transform(self) -> None:
        """
        Основная бизнес-логика добавления товара в корзину.

        Выполняет следующие операции в строгой последовательности:
        1. Находит существующую корзину пользователя или создает новую
        2. Ищет существующий элемент корзины с такими же product_id и variant_id
        3. Если товар уже есть в корзине:
           - Увеличивает количество на запрашиваемое
           - Проверяет не превышает ли итоговое количество доступный stock
           - Обновляет delta_price актуальным значением из варианта
           - Сохраняет обновленный элемент корзины
        4. Если товара нет в корзине:
           - Создает новый элемент корзины с правильными ценами
           - Устанавливает SKU из варианта или товара
           - Сохраняет новый элемент в базу данных

        Raises:
            AppExceptionResponse: При ошибках:
                - bad_request: Если не удалось создать корзину
                - bad_request: Если итоговое количество превышает stock

        Note:
            Метод работает с уже валидированными данными из validate() метода.
            Использует computed поля для автоматического расчета unit_price и total_price.
            Корректно обрабатывает случаи с variant_id=None (товары без вариантов).
        """
        # Ищем существующую корзину пользователя
        self.cart_entity = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == self.current_user.id]
        )

        # Если корзины нет - создаем новую
        if not self.cart_entity:
            await self.cart_repository.create(CartEntity(user_id=self.current_user.id))
            self.cart_entity = await self.cart_repository.get_first_with_filters(
                filters=[self.cart_repository.model.user_id == self.current_user.id]
            )

        # Проверяем, что корзина успешно создана/найдена
        if not self.cart_entity:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("cart_not_found"))

        # Ищем существующий элемент корзины с таким же product_id и variant_id
        # Учитываем, что variant_id может быть None (товар без вариантов)
        self.cart_item_entity = await self.cart_item_repository.get_first_with_filters(
            filters=[
                and_(
                    self.cart_item_repository.model.cart_id == self.cart_entity.id,
                    self.cart_item_repository.model.product_id == self.current_product.id,
                    (
                        self.cart_item_repository.model.variant_id == self.current_product_variant_entity.id
                        if self.current_product_variant_entity
                        else self.cart_item_repository.model.variant_id.is_(None)
                    )
                )
            ]
        )

        # Если товар уже есть в корзине - обновляем количество
        if self.cart_item_entity:
            # Создаем DTO из существующего элемента для обновления
            cdto = CartItemCDTO.from_orm(self.cart_item_entity)
            cdto.qty += self.dto.qty  # Увеличиваем количество на запрашиваемое

            # Проверяем, что итоговое количество не превышает stock
            available_stock = (
                self.current_product_variant_entity.stock
                if self.current_product_variant_entity
                else self.current_product.stock
            )
            if cdto.qty > available_stock:
                raise AppExceptionResponse.bad_request(message=i18n.gettext("product_not_available"))

            # Обновляем delta_price актуальным значением из варианта
            if self.current_product_variant_entity:
                cdto.delta_price = self.current_product_variant_entity.price_delta
            else:
                cdto.delta_price = Decimal("0.00")

            # Сохраняем обновленный элемент корзины
            await self.cart_item_repository.update(obj=self.cart_item_entity, dto=cdto)

        # Если товара нет в корзине - создаем новый элемент
        else:
            new_cart_item = CartItemEntity(
                cart_id=self.cart_entity.id,
                product_id=self.current_product.id,
                variant_id=self.current_product_variant_entity.id if self.current_product_variant_entity else None,
                product_price=self.current_product.base_price,  # Базовая цена товара
                delta_price=self.current_product_variant_entity.price_delta if self.current_product_variant_entity else Decimal("0.00"),  # Доплата за вариант
                sku=self.current_product_variant_entity.sku if self.current_product_variant_entity else self.current_product.sku,  # SKU варианта или товара
                qty=self.dto.qty  # Запрашиваемое количество
            )
            await self.cart_item_repository.create(new_cart_item)