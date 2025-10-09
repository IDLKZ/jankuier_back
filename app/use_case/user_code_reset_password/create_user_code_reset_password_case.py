from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_reset_password.user_code_reset_password_dto import (
    UserCodeResetPasswordCDTO,
    UserCodeResetPasswordWithRelationsRDTO,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateUserCodeResetPasswordCase(BaseUseCase[UserCodeResetPasswordWithRelationsRDTO]):
    """
    Класс Use Case для создания нового кода сброса пароля.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.
        - Репозиторий `UserRepository` для проверки существования пользователя.
        - DTO `UserCodeResetPasswordCDTO` для входных данных.
        - DTO `UserCodeResetPasswordWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.
        user_repository (UserRepository): Репозиторий для работы с пользователями.
        model (UserCodeResetPasswordEntity | None): Созданная модель кода сброса пароля.

    Методы:
        execute(dto: UserCodeResetPasswordCDTO) -> UserCodeResetPasswordWithRelationsRDTO:
            Создает новый код сброса пароля и возвращает DTO.
        validate(dto: UserCodeResetPasswordCDTO):
            Проверяет корректность входных данных.
        transform(dto: UserCodeResetPasswordCDTO):
            Преобразует DTO в модель.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserCodeResetPasswordRepository(db)
        self.user_repository = UserRepository(db)
        self.model: UserCodeResetPasswordEntity | None = None

    async def execute(
        self, dto: UserCodeResetPasswordCDTO
    ) -> UserCodeResetPasswordWithRelationsRDTO:
        """
        Выполняет операцию создания кода сброса пароля.

        Args:
            dto (UserCodeResetPasswordCDTO): Данные для создания кода.

        Returns:
            UserCodeResetPasswordWithRelationsRDTO: Созданный код с связями.

        Raises:
            AppExceptionResponse: Если пользователь не найден.
        """
        await self.validate(dto)
        await self.transform(dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return UserCodeResetPasswordWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: UserCodeResetPasswordCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (UserCodeResetPasswordCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если пользователь не найден.
        """
        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

    async def transform(self, dto: UserCodeResetPasswordCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (UserCodeResetPasswordCDTO): Данные для преобразования.
        """
        self.model = UserCodeResetPasswordEntity(**dto.dict())
