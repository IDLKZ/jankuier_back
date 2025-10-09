from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_reset_password.user_code_reset_password_dto import (
    PaginationUserCodeResetPasswordRDTO,
    UserCodeResetPasswordWithRelationsRDTO,
)
from app.adapters.filters.user_code_reset_password.user_code_reset_password_pagination_filter import (
    UserCodeResetPasswordPaginationFilter,
)
from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateUserCodeResetPasswordCase(BaseUseCase[PaginationUserCodeResetPasswordRDTO]):
    """
    Класс Use Case для получения кодов сброса пароля с пагинацией.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.
        - DTO `UserCodeResetPasswordWithRelationsRDTO` для возврата данных с связями.
        - `PaginationUserCodeResetPasswordRDTO` для пагинированного ответа.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.

    Методы:
        execute() -> PaginationUserCodeResetPasswordRDTO:
            Выполняет запрос и возвращает пагинированный список кодов.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserCodeResetPasswordRepository(db)

    async def execute(
        self, filter: UserCodeResetPasswordPaginationFilter
    ) -> PaginationUserCodeResetPasswordRDTO:
        """
        Выполняет операцию получения кодов сброса пароля с пагинацией.

        Args:
            filter (UserCodeResetPasswordPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationUserCodeResetPasswordRDTO: Пагинированный список кодов с связями.
        """
        models = await self.repository.paginate(
            dto=UserCodeResetPasswordWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
