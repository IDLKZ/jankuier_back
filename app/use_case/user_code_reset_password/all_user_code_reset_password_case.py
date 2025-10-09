from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_reset_password.user_code_reset_password_dto import (
    UserCodeResetPasswordWithRelationsRDTO,
)
from app.adapters.filters.user_code_reset_password.user_code_reset_password_filter import (
    UserCodeResetPasswordFilter,
)
from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.use_case.base_case import BaseUseCase


class AllUserCodeResetPasswordCase(BaseUseCase[list[UserCodeResetPasswordWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех кодов сброса пароля.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.
        - DTO `UserCodeResetPasswordWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.

    Методы:
        execute() -> list[UserCodeResetPasswordWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех кодов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserCodeResetPasswordRepository(db)

    async def execute(
        self, filter: UserCodeResetPasswordFilter
    ) -> list[UserCodeResetPasswordWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех кодов сброса пароля.

        Args:
            filter (UserCodeResetPasswordFilter): Фильтр для поиска и сортировки.

        Returns:
            list[UserCodeResetPasswordWithRelationsRDTO]: Список объектов кодов с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
        )
        return [UserCodeResetPasswordWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
