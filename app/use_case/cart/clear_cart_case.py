from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class ClearCartCase(BaseUseCase[CartWithRelationsRDTO]):
    """
    Use Case для полной очистки корзины пользователя.
    Удаляет все товары из корзины, но саму корзину оставляет.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(self, user_id: int) -> CartWithRelationsRDTO:
        """
        Очищает корзину пользователя от всех товаров.
        
        Args:
            user_id: ID пользователя
        
        Returns:
            CartWithRelationsRDTO: Пустая корзина пользователя
        """
        await self.validate(user_id)
        
        # Получаем корзину пользователя
        cart = await self._get_user_cart(user_id)
        
        # Удаляем все товары из корзины
        await self._remove_all_cart_items(cart.id)
        
        # Обновляем корзину - обнуляем итоги
        cart.total_price = Decimal("0.00")
        cart.cart_items = {}
        await self.cart_repository.update_obj(cart)
        
        # Возвращаем очищенную корзину
        updated_cart = await self.cart_repository.get(
            cart.id, 
            options=self.cart_repository.default_relationships()
        )
        
        return CartWithRelationsRDTO.from_orm(updated_cart)

    async def validate(self, user_id: int) -> None:
        """Валидация входных данных"""
        
        if not isinstance(user_id, int) or user_id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("user_id_validation_error")
            )
        
        # Проверяем существование пользователя
        user = await self.user_repository.get(user_id)
        if not user:
            raise AppExceptionResponse.not_found(
                i18n.gettext("user_not_found")
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

    async def _remove_all_cart_items(self, cart_id: int) -> None:
        """Удаляет все товары из корзины"""
        
        # Получаем все элементы корзины
        cart_items = await self.cart_item_repository.get_with_filters(
            filters=[self.cart_item_repository.model.cart_id == cart_id]
        )
        
        # Удаляем каждый элемент
        for cart_item in cart_items:
            await self.cart_item_repository.delete(cart_item.id)