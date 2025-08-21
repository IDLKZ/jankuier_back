from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCartByIdCase(BaseUseCase[CartRDTO]):
    """
    Класс Use Case для получения корзины по ID.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - DTO `CartRDTO` для возврата данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.

    Методы:
        execute() -> CartRDTO:
            Выполняет запрос и возвращает корзину по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartRepository(db)

    async def execute(self, id: int) -> CartRDTO:
        """
        Выполняет операцию получения корзины по ID.

        Args:
            id (int): ID корзины.

        Returns:
            CartRDTO: Объект корзины.

        Raises:
            AppExceptionResponse: Если корзина не найдена.
        """
        await self.validate(id)
        
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("cart_not_found")
            )
        
        return CartRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID корзины для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("cart_id_validation_error")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass