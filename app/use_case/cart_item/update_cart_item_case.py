from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import CartItemUpdateDTO, CartItemWithRelationsRDTO
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CartItemEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateCartItemCase(BaseUseCase[CartItemWithRelationsRDTO]):
    """
    Класс Use Case для обновления товара в корзине.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.
        - DTO `CartItemUpdateDTO` для входных данных.
        - DTO `CartItemWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.
        model (CartItemEntity | None): Обновляемая модель товара в корзине.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)
        self.model: CartItemEntity | None = None

    async def execute(
        self, id: int, dto: CartItemUpdateDTO
    ) -> CartItemWithRelationsRDTO:
        """
        Выполняет операцию обновления товара в корзине.

        Args:
            id (int): Идентификатор товара в корзине.
            dto (CartItemUpdateDTO): Данные для обновления товара в корзине.

        Returns:
            CartItemWithRelationsRDTO: Обновленный товар в корзине с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return CartItemWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: CartItemUpdateDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор товара в корзине.
            dto (CartItemUpdateDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования товара в корзине
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("cart_item_not_found")
            )

        # Валидация количества (если обновляется)
        if dto.qty is not None and dto.qty <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cart_item_quantity_invalid")
            )

        # Валидация дельты цены (delta_price может быть отрицательной для скидок)
        # Но общая цена за единицу не должна быть отрицательной
        if dto.delta_price is not None:
            expected_unit_price = model.product_price + dto.delta_price
            if expected_unit_price < Decimal('0'):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("cart_item_price_invalid")
                )

    async def transform(self, id: int, dto: CartItemUpdateDTO) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор товара в корзине.
            dto (CartItemUpdateDTO): Данные для преобразования.
        """
        self.model = await self.repository.get(id)

        # Автоматический пересчет цен при обновлении количества или дельты
        current_qty = dto.qty if dto.qty is not None else self.model.qty
        current_delta_price = dto.delta_price if dto.delta_price is not None else self.model.delta_price
        
        # Пересчитываем unit_price и total_price
        new_unit_price = self.model.product_price + current_delta_price
        new_total_price = new_unit_price * current_qty

        # Обновляем DTO с пересчитанными значениями
        dto.unit_price = new_unit_price
        dto.total_price = new_total_price