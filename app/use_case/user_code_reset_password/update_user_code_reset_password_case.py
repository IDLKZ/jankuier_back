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


class UpdateUserCodeResetPasswordCase(BaseUseCase[UserCodeResetPasswordWithRelationsRDTO]):
    """
    Класс Use Case для обновления кода сброса пароля.

    Использует:
        - Репозиторий `UserCodeResetPasswordRepository` для работы с базой данных.
        - Репозиторий `UserRepository` для проверки существования пользователя.
        - DTO `UserCodeResetPasswordCDTO` для входных данных.
        - DTO `UserCodeResetPasswordWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (UserCodeResetPasswordRepository): Репозиторий для работы с кодами сброса пароля.
        user_repository (UserRepository): Репозиторий для работы с пользователями.
        model (UserCodeResetPasswordEntity | None): Обновляемая модель кода сброса пароля.

    Методы:
        execute(id: int, dto: UserCodeResetPasswordCDTO) -> UserCodeResetPasswordWithRelationsRDTO:
            Обновляет код сброса пароля и возвращает DTO.
        validate(id: int, dto: UserCodeResetPasswordCDTO):
            Проверяет существование кода и корректность данных.
        transform(dto: UserCodeResetPasswordCDTO):
            Преобразует входные данные.
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
        self, id: int, dto: UserCodeResetPasswordCDTO
    ) -> UserCodeResetPasswordWithRelationsRDTO:
        """
        Выполняет операцию обновления кода сброса пароля.

        Args:
            id (int): Идентификатор кода сброса пароля.
            dto (UserCodeResetPasswordCDTO): Данные для обновления кода.

        Returns:
            UserCodeResetPasswordWithRelationsRDTO: Обновленный код с связями.

        Raises:
            AppExceptionResponse: Если код или пользователь не найдены.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return UserCodeResetPasswordWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: UserCodeResetPasswordCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор кода для проверки.
            dto (UserCodeResetPasswordCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если код или пользователь не найдены.
        """
        # Проверка существования кода
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

    async def transform(self, dto: UserCodeResetPasswordCDTO) -> None:
        """
        Преобразование входных данных.

        Args:
            dto (UserCodeResetPasswordCDTO): Данные для преобразования.
        """
        # Дополнительные преобразования можно добавить здесь при необходимости
        pass
