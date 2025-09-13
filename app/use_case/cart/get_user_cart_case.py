from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetUserCartCase(BaseUseCase[CartWithRelationsRDTO]):
    """
    Use Case для получения корзины пользователя с автоматическим созданием, если её нет.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.cart_repository = CartRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(
        self, 
        user_id: int,
        create_if_not_exists: bool = True
    ) -> CartWithRelationsRDTO | None:
        """
        Получает корзину пользователя.
        
        Args:
            user_id: ID пользователя
            create_if_not_exists: Создать корзину, если её нет
        
        Returns:
            CartWithRelationsRDTO | None: Корзина пользователя или None
        """
        await self.validate(user_id)
        
        # Ищем существующую корзину
        cart = await self.cart_repository.get_first_with_filters(
            filters=[self.cart_repository.model.user_id == user_id],
            include_deleted_filter=True,
            options=self.cart_repository.default_relationships()
        )
        
        if cart:
            # Пересчитываем итоги на случай изменения цен товаров
            await self._sync_cart_totals(cart)
            # Перезагружаем корзину после синхронизации
            cart = await self.cart_repository.get(
                cart.id, 
                options=self.cart_repository.default_relationships()
            )
            return CartWithRelationsRDTO.from_orm(cart)
        
        if create_if_not_exists:
            # Создаем новую пустую корзину
            cart_data = CartEntity(
                user_id=user_id,
                total_price=Decimal("0.00"),
                cart_items={}
            )
            cart = await self.cart_repository.create(cart_data)
            cart = await self.cart_repository.get(
                cart.id, 
                options=self.cart_repository.default_relationships()
            )
            return CartWithRelationsRDTO.from_orm(cart)
        
        return None

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

    async def _sync_cart_totals(self, cart: CartEntity) -> None:
        """
        Синхронизирует итоги корзины с актуальными данными товаров.
        Это нужно на случай, если цены товаров изменились после добавления в корзину.
        """
        if not hasattr(cart, 'cart_items_list') or not cart.cart_items_list:
            # Корзина пуста, обновляем итоги
            cart.total_price = Decimal("0.00")
            cart.cart_items = {}
            await self.cart_repository.update_obj(cart)
            return
        
        # Пересчитываем общую стоимость на основе элементов корзины
        total_price = Decimal("0.00")
        cart_snapshot = {}
        
        for cart_item in cart.cart_items_list:
            # Используем актуальные данные из cart_item
            total_price += cart_item.total_price
            
            # Обновляем snapshot
            cart_snapshot[str(cart_item.id)] = {
                "product_id": cart_item.product_id,
                "variant_id": cart_item.variant_id,
                "qty": cart_item.qty,
                "unit_price": float(cart_item.unit_price),
                "total_price": float(cart_item.total_price),
                "sku": cart_item.sku
            }
        
        # Обновляем корзину если данные изменились
        if cart.total_price != total_price or cart.cart_items != cart_snapshot:
            cart.total_price = total_price
            cart.cart_items = cart_snapshot
            await self.cart_repository.update_obj(cart)