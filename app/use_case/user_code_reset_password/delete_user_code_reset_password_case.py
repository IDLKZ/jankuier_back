from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteUserCodeResetPasswordCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления кода сброса пароля по ID.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.
        model (UserCodeResetPasswordEntity | None): Удаляемая модель кода.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет код и возвращает результат операции.
        validate(id: int):
            Проверяет существование кода.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserCodeResetPasswordRepository(db)
        self.model: UserCodeResetPasswordEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления кода сброса пароля.

        Args:
            id (int): Идентификатор кода.
            force_delete (bool): Принудительное удаление (по умолчанию False).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если код не найден.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор кода для проверки.

        Raises:
            AppExceptionResponse: Если код не найден.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
