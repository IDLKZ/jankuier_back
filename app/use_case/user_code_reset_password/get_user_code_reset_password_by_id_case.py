from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_reset_password.user_code_reset_password_dto import (
    UserCodeResetPasswordWithRelationsRDTO,
)
from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetUserCodeResetPasswordByIdCase(BaseUseCase[UserCodeResetPasswordWithRelationsRDTO]):
    """
    Класс Use Case для получения кода сброса пароля по ID.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.
        - DTO `UserCodeResetPasswordWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.
        model (UserCodeResetPasswordEntity | None): Найденная модель кода.

    Методы:
        execute(id: int) -> UserCodeResetPasswordWithRelationsRDTO:
            Выполняет поиск кода по ID и возвращает DTO.
        validate(id: int):
            Проверяет существование кода с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserCodeResetPasswordRepository(db)
        self.model: UserCodeResetPasswordEntity | None = None

    async def execute(self, id: int) -> UserCodeResetPasswordWithRelationsRDTO:
        """
        Выполняет операцию получения кода сброса пароля по ID.

        Args:
            id (int): Идентификатор кода.

        Returns:
            UserCodeResetPasswordWithRelationsRDTO: Объект кода с связями.

        Raises:
            AppExceptionResponse: Если код не найден.
        """
        await self.validate(id=id)
        return UserCodeResetPasswordWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор кода для проверки.

        Raises:
            AppExceptionResponse: Если код не найден.
        """
        self.model = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
