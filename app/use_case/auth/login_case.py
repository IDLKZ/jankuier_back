from app.adapters.dto.auth.login_dto import LoginDTO
from app.adapters.dto.auth.token_dto import BearerTokenDTO
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class LoginCase(BaseUseCase[BearerTokenDTO]):
    """
    Use case для аутентификации пользователей.

    Атрибуты:
        repository (UserRepository): Репозиторий для работы с пользователями.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализирует use case с сессией базы данных.

        Аргументы:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = UserRepository(db)

    async def execute(self, dto: LoginDTO) -> BearerTokenDTO:
        """
        Выполняет аутентификацию пользователя.

        Аргументы:
            dto (LoginDTO): DTO с учетными данными пользователя.

        Возвращает:
            BearerTokenDTO: DTO с токенами доступа и обновления.

        Вызывает:
            AppExceptionResponse.bad_request: Если введены неверные данные.
        """
        user = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    func.lower(self.repository.model.username) == dto.username.lower(),
                )
            ]
        )
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("data_not_ready")
            )
        if not user.is_active:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_active")
            )
        result = verify_password(dto.password, user.password_hash)
        if not result:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("data_not_ready")
            )
        access_token = create_access_token(data=user.id)
        refresh_token = create_refresh_token(data=user.id)
        return BearerTokenDTO(access_token=access_token, refresh_token=refresh_token)

    async def validate(self) -> None:
        """
        Заглушка для потенциальной логики валидации.
        """
