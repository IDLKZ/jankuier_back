from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import CartRDTO
from app.adapters.repository.cart.cart_repository import CartRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetCartByUserIdCase(BaseUseCase[CartRDTO]):
    """
    Класс Use Case для получения корзины по ID пользователя.

    Использует:
        - Репозиторий `CartRepository` для работы с базой данных.
        - Репозиторий `UserRepository` для проверки существования пользователя.
        - DTO `CartRDTO` для возврата данных.

    Атрибуты:
        repository (CartRepository): Репозиторий для работы с корзинами.
        user_repository (UserRepository): Репозиторий для работы с пользователями.

    Методы:
        execute() -> CartRDTO:
            Выполняет запрос и возвращает корзину пользователя.
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
        self.user_repository = UserRepository(db)

    async def execute(self, user_id: int) -> CartRDTO:
        """
        Выполняет операцию получения корзины по ID пользователя.

        Args:
            user_id (int): ID пользователя.

        Returns:
            CartRDTO: Объект корзины пользователя.

        Raises:
            AppExceptionResponse: Если корзина не найдена.
        """
        await self.validate(user_id)

        # Ищем активную корзину пользователя
        model = await self.repository.get_first_with_filters(
            filters=[self.repository.model.user_id == user_id],
            include_deleted_filter=True,
        )

        if not model:
            raise AppExceptionResponse.not_found(i18n.gettext("cart_not_found"))

        return CartRDTO.from_orm(model)

    async def validate(self, user_id: int) -> None:
        """
        Валидация входных данных.

        Args:
            user_id (int): ID пользователя для валидации.

        Raises:
            AppExceptionResponse: Если ID пользователя недействителен или пользователь не найден.
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("user_id_validation_error")
            )

        # Проверяем существование пользователя
        user = await self.user_repository.get(user_id)
        if not user:
            raise AppExceptionResponse.not_found(i18n.gettext("user_not_found"))

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
