from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartRDTO, CartWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_variant.product_variant_repository import (
    ProductVariantRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity, CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class AddToCartCase(BaseUseCase[CartWithRelationsRDTO]):
    """
    Use Case для добавления товара в корзину пользователя.
    Автоматически создает корзину, если её нет, или добавляет товар в существующую.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.product_repository = ProductRepository(db)
        self.variant_repository = ProductVariantRepository(db)
        self.db = db

    async def execute(
        self, 
        user_id: int,
        product_id: int, 
        qty: int = 1,
        variant_id: int | None = None
    ) -> CartWithRelationsRDTO:
        """
        Добавляет товар в корзину пользователя.
        
        Args:
            user_id: ID пользователя
            product_id: ID товара
            qty: Количество товара (по умолчанию 1)
            variant_id: ID варианта товара (опционально)
        
        Returns:
            CartWithRelationsRDTO: Обновленная корзина с товарами
        """
        await self.validate(user_id, product_id, qty, variant_id)
        
        # Получаем или создаем корзину
        cart = await self._get_or_create_cart(user_id)
        
        # Получаем товар для расчета цены
        product = await self.product_repository.get(
            product_id, 
            options=self.product_repository.default_relationships()
        )
        
        # Получаем вариант если указан
        variant = None
        if variant_id:
            variant = await self.variant_repository.get(variant_id)
        
        # Проверяем, есть ли уже такой товар в корзине
        existing_item = await self.cart_item_repository.get_first_with_filters(
            filters=[
                self.cart_item_repository.model.cart_id == cart.id,
                self.cart_item_repository.model.product_id == product_id,
                self.cart_item_repository.model.variant_id == variant_id,
            ]
        )
        
        if existing_item:
            # Обновляем количество существующего товара
            new_qty = existing_item.qty + qty
            await self._update_cart_item_qty(existing_item, new_qty, product, variant)
        else:
            # Создаем новый элемент корзины
            await self._create_cart_item(cart, product, variant, qty)
        
        # Пересчитываем общую стоимость корзины
        await self._recalculate_cart_total(cart.id)
        
        # Возвращаем обновленную корзину
        updated_cart = await self.cart_repository.get(
            cart.id, 
            options=self.cart_repository.default_relationships()
        )
        
        return CartWithRelationsRDTO.from_orm(updated_cart)

    async def validate(
        self, 
        user_id: int, 
        product_id: int, 
        qty: int, 
        variant_id: int | None = None
    ) -> None:
        """Валидация входных данных"""
        
        if not isinstance(user_id, int) or user_id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("user_id_validation_error")
            )
        
        if not isinstance(product_id, int) or product_id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("product_id_validation_error")
            )
        
        if not isinstance(qty, int) or qty <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("cart_item_quantity_invalid")
            )
        
        # Проверяем существование товара
        product = await self.product_repository.get(product_id)
        if not product:
            raise AppExceptionResponse.not_found(
                i18n.gettext("product_not_found")
            )
        
        # Проверяем вариант, если указан
        if variant_id:
            if not isinstance(variant_id, int) or variant_id <= 0:
                raise AppExceptionResponse.bad_request(
                    i18n.gettext("variant_id_validation_error")
                )
            
            variant = await self.variant_repository.get(variant_id)
            if not variant:
                raise AppExceptionResponse.not_found(
                    i18n.gettext("product_variant_not_found")
                )
            
            if variant.product_id != product_id:
                raise AppExceptionResponse.bad_request(
                    i18n.gettext("product_variant_mismatch")
                )

    async def transform(self) -> None:
        """Не используется в данном use case"""
        pass

    async def _get_or_create_cart(self, user_id: int) -> CartEntity:
        """Получает существующую корзину или создает новую для пользователя"""
        
        # Ищем активную корзину пользователя
        cart = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == user_id],
            include_deleted_filter=True,
        )
        
        if not cart:
            # Создаем новую корзину
            cart_data = CartEntity(
                user_id=user_id,
                total_price=Decimal("0.00"),
                cart_items={}
            )
            cart = await self.cart_repository.create(cart_data)
            await self.cart_repository.refresh(cart)
        
        return cart

    async def _create_cart_item(
        self, 
        cart: CartEntity, 
        product, 
        variant, 
        qty: int
    ) -> None:
        """Создает новый элемент корзины"""
        
        # Определяем цены
        base_price = variant.price if variant else product.price
        delta_price = Decimal("0.00")  # Можно добавить логику для скидок/надбавок
        unit_price = base_price + delta_price
        total_price = unit_price * qty
        
        # Определяем SKU
        sku = variant.sku if variant else getattr(product, 'sku', None)
        
        # Создаем элемент корзины
        cart_item_data = CartItemEntity(
            cart_id=cart.id,
            product_id=product.id,
            variant_id=variant.id if variant else None,
            qty=qty,
            sku=sku,
            product_price=base_price,
            delta_price=delta_price,
            unit_price=unit_price,
            total_price=total_price
        )
        
        await self.cart_item_repository.create(cart_item_data)

    async def _update_cart_item_qty(
        self, 
        cart_item: CartItemEntity, 
        new_qty: int, 
        product, 
        variant
    ) -> None:
        """Обновляет количество товара в корзине и пересчитывает цены"""
        
        # Получаем актуальную цену товара
        base_price = variant.price if variant else product.price
        delta_price = cart_item.delta_price  # Сохраняем существующую дельту
        unit_price = base_price + delta_price
        total_price = unit_price * new_qty
        
        # Обновляем элемент корзины
        cart_item.qty = new_qty
        cart_item.product_price = base_price
        cart_item.unit_price = unit_price
        cart_item.total_price = total_price
        
        await self.cart_item_repository.update_obj(cart_item)

    async def _recalculate_cart_total(self, cart_id: int) -> None:
        """Пересчитывает общую стоимость корзины"""
        
        # Получаем все элементы корзины
        cart_items = await self.cart_item_repository.get_with_filters(
            filters=[self.cart_item_repository.model.cart_id == cart_id]
        )
        
        # Считаем общую стоимость
        total_price = sum(item.total_price for item in cart_items)
        
        # Обновляем корзину
        cart = await self.cart_repository.get(cart_id)
        cart.total_price = total_price
        
        # Сохраняем snapshot товаров в JSONB поле
        cart_snapshot = {}
        for item in cart_items:
            cart_snapshot[str(item.id)] = {
                "product_id": item.product_id,
                "variant_id": item.variant_id,
                "qty": item.qty,
                "unit_price": float(item.unit_price),
                "total_price": float(item.total_price),
                "sku": item.sku
            }
        cart.cart_items = cart_snapshot
        
        await self.cart_repository.update_obj(cart)