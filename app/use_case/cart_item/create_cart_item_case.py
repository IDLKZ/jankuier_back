from decimal import Decimal
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import (
    CartItemCDTO,
    CartItemWithRelationsRDTO,
)
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_variant.product_variant_repository import (
    ProductVariantRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateCartItemCase(BaseUseCase[CartItemWithRelationsRDTO]):
    """
    Класс Use Case для создания нового товара в корзине.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.
        - Репозиторий `CartRepository` для проверки существования корзины.
        - Репозиторий `ProductRepository` для проверки существования товара.
        - Репозиторий `ProductVariantRepository` для проверки существования варианта товара.
        - DTO `CartItemCDTO` для входных данных.
        - DTO `CartItemWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.
        cart_repository (CartRepository): Репозиторий для работы с корзинами.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        variant_repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        model (CartItemEntity | None): Созданная модель товара в корзине.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)
        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)
        self.variant_repository = ProductVariantRepository(db)
        self.model: CartItemEntity | None = None

    async def execute(self, dto: CartItemCDTO) -> CartItemWithRelationsRDTO:
        """
        Выполняет операцию создания товара в корзине.

        Args:
            dto (CartItemCDTO): Данные для создания товара в корзине.

        Returns:
            CartItemWithRelationsRDTO: Созданный товар в корзине с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return CartItemWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: CartItemCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (CartItemCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования корзины
        cart = await self.cart_repository.get(dto.cart_id)
        if not cart:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_not_found")
            )

        # Проверка существования товара
        product = await self.product_repository.get(dto.product_id)
        if not product:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_not_found")
            )

        # Проверка существования варианта товара (если указан)
        if dto.variant_id:
            variant = await self.variant_repository.get(dto.variant_id)
            if not variant:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_not_found")
                )

            # Проверка, что вариант принадлежит указанному товару
            if variant.product_id != dto.product_id:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("product_variant_not_found")
                )

        # Валидация количества
        if dto.qty <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_quantity_invalid")
            )

        # Валидация цен
        if dto.product_price < Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_price_invalid")
            )

        if dto.unit_price < Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_price_invalid")
            )

        if dto.total_price < Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_price_invalid")
            )

        # Проверка математической корректности цен
        expected_unit_price = dto.product_price + dto.delta_price
        expected_total_price = expected_unit_price * dto.qty

        if abs(dto.unit_price - expected_unit_price) > Decimal("0.01"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_calculation_error")
            )

        if abs(dto.total_price - expected_total_price) > Decimal("0.01"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_calculation_error")
            )

        # Проверка на дублирование: один товар с одним вариантом не может быть дважды в корзине
        existing_item = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.cart_id == dto.cart_id,
                self.repository.model.product_id == dto.product_id,
                self.repository.model.variant_id == dto.variant_id,
            ]
        )
        if existing_item:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_duplicate")
            )

    async def transform(self, dto: CartItemCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (CartItemCDTO): Данные для преобразования.
        """
        # Автоматический расчет цен (если они не были рассчитаны правильно)
        dto.unit_price = dto.product_price + dto.delta_price
        dto.total_price = dto.unit_price * dto.qty

        # Если SKU не указан, можно автоматически сгенерировать на основе продукта и варианта
        if not dto.sku:
            if dto.variant_id:
                # Получаем вариант для формирования SKU
                variant = await self.variant_repository.get(dto.variant_id)
                if variant and variant.sku:
                    dto.sku = variant.sku
            else:
                # Получаем товар для формирования SKU
                product = await self.product_repository.get(dto.product_id)
                if product and hasattr(product, "sku") and product.sku:
                    dto.sku = product.sku

        self.model = CartItemEntity(**dto.dict())
