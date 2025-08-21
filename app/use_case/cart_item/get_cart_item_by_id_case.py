from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import CartItemRDTO
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCartItemByIdCase(BaseUseCase[CartItemRDTO]):
    """
    Класс Use Case для получения товара в корзине по ID.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.
        - DTO `CartItemRDTO` для возврата данных.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.

    Методы:
        execute() -> CartItemRDTO:
            Выполняет запрос и возвращает товар в корзине по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)

    async def execute(self, id: int) -> CartItemRDTO:
        """
        Выполняет операцию получения товара в корзине по ID.

        Args:
            id (int): ID товара в корзине.

        Returns:
            CartItemRDTO: Объект товара в корзине.

        Raises:
            AppExceptionResponse: Если товар в корзине не найден.
        """
        await self.validate(id)
        
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("cart_item_not_found")
            )
        
        return CartItemRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID товара в корзине для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("cart_item_id_validation_error")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass