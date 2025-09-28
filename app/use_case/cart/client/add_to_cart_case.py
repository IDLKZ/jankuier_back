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

    Функциональность:
    - Создает корзину если её нет
    - Проверяет доступность товара и варианта
    - Увеличивает количество если товар уже в корзине
    - Создает новый элемент корзины если товара нет
    - Проверяет stock перед добавлением
    """

    def __init__(self, db: AsyncSession) -> None:
        # Инициализация репозиториев для работы с данными
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
        self.product_item_repository = ProductVariantRepository(db)

        # Переменные для хранения сущностей, полученных в процессе выполнения
        self.cart_entity: CartEntity | None = None  # Корзина пользователя
        self.cart_item_entity: CartItemEntity | None = None  # Существующий элемент корзины (если есть)
        self.cart_items_entity: List[CartItemEntity] | None = []  # Корзина пользователя
        self.current_product: ProductEntity | None = None  # Добавляемый товар
        self.current_product_variant_entity: ProductVariantEntity | None = None  # Вариант товара (если есть)

        # Входные данные для обработки
        self.dto: AddToCartDTO | None = None  # DTO с данными о добавляемом товаре
        self.current_user: UserWithRelationsRDTO | None = None  # Текущий пользователь

    async def execute(self, dto: AddToCartDTO, user: UserWithRelationsRDTO) -> CartActionResponseDTO:
        """
        Основной метод выполнения добавления товара в корзину.

        Args:
            dto: DTO с данными о добавляемом товаре (product_id, variant_id, qty)
            user: Текущий пользователь

        Returns:
            CartActionResponseDTO: Ответ с корзиной, элементами и общей стоимостью
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

        Проверяет:
        1. Наличие обязательных параметров (dto и user)
        2. Существование и доступность товара
        3. Если указан variant_id - существование и доступность варианта
        4. Достаточность stock для запрашиваемого количества

        Raises:
            AppExceptionResponse: При любой ошибке валидации
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

        Выполняет следующие операции:
        1. Находит существующую корзину пользователя или создает новую
        2. Проверяет, есть ли уже такой товар (с таким же variant) в корзине
        3. Если товар есть - увеличивает количество
        4. Если товара нет - создает новый элемент корзины
        5. Проверяет limits по stock при обновлении количества

        Raises:
            AppExceptionResponse: При ошибке создания корзины или превышении stock
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