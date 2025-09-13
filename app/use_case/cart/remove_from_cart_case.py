from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class RemoveFromCartCase(BaseUseCase[CartWithRelationsRDTO]):
    """
    Use Case для удаления товара из корзины пользователя.
    Может удалить товар полностью или уменьшить количество.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.db = db

    async def execute(
        self, 
        user_id: int,
        product_id: int, 
        qty_to_remove: int | None = None,
        variant_id: int | None = None,
        remove_completely: bool = False
    ) -> CartWithRelationsRDTO:
        """
        Удаляет товар из корзины пользователя.
        
        Args:
            user_id: ID пользователя
            product_id: ID товара
            qty_to_remove: Количество для удаления (если None, удаляет полностью)
            variant_id: ID варианта товара (опционально)
            remove_completely: Флаг полного удаления товара
        
        Returns:
            CartWithRelationsRDTO: Обновленная корзина с товарами
        """
        await self.validate(user_id, product_id, qty_to_remove, variant_id)
        
        # Получаем корзину пользователя
        cart = await self._get_user_cart(user_id)
        
        # Находим товар в корзине
        cart_item = await self.cart_item_repository.get_first_with_filters(
            filters=[
                self.cart_item_repository.model.cart_id == cart.id,
                self.cart_item_repository.model.product_id == product_id,
                self.cart_item_repository.model.variant_id == variant_id,
            ]
        )
        
        if not cart_item:
            raise AppExceptionResponse.not_found(
                i18n.gettext("cart_item_not_found")
            )
        
        # Определяем, что делать с товаром
        if remove_completely or qty_to_remove is None or qty_to_remove >= cart_item.qty:
            # Удаляем товар полностью
            await self.cart_item_repository.delete(cart_item.id)
        else:
            # Уменьшаем количество
            new_qty = cart_item.qty - qty_to_remove
            await self._update_cart_item_qty(cart_item, new_qty)
        
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
        qty_to_remove: int | None = None,
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
        
        if qty_to_remove is not None:
            if not isinstance(qty_to_remove, int) or qty_to_remove <= 0:
                raise AppExceptionResponse.bad_request(
                    i18n.gettext("cart_item_quantity_invalid")
                )
        
        if variant_id is not None:
            if not isinstance(variant_id, int) or variant_id <= 0:
                raise AppExceptionResponse.bad_request(
                    i18n.gettext("variant_id_validation_error")
                )

    async def transform(self) -> None:
        """Не используется в данном use case"""
        pass

    async def _get_user_cart(self, user_id: int):
        """Получает корзину пользователя"""
        
        cart = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == user_id],
            include_deleted_filter=True,
        )
        
        if not cart:
            raise AppExceptionResponse.not_found(
                i18n.gettext("cart_not_found")
            )
        
        return cart

    async def _update_cart_item_qty(self, cart_item, new_qty: int) -> None:
        """Обновляет количество товара в корзине и пересчитывает цены"""
        
        # Пересчитываем общую стоимость для этого товара
        total_price = cart_item.unit_price * new_qty
        
        # Обновляем элемент корзины
        cart_item.qty = new_qty
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
        
        # Обновляем snapshot товаров в JSONB поле
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