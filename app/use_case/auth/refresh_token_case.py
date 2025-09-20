from datetime import datetime

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.token_dto import BearerTokenDTO
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import create_access_token, create_refresh_token
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.use_case.base_case import BaseUseCase


class RefreshTokenCase(BaseUseCase[BearerTokenDTO]):
    """
    Use case для обновления токенов доступа с помощью refresh token.

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

    async def execute(self, refresh_token: str) -> BearerTokenDTO:
        """
        Выполняет обновление токенов доступа.

        Аргументы:
            refresh_token (str): Refresh token для обновления.

        Возвращает:
            BearerTokenDTO: DTO с новыми токенами доступа и обновления.

        Вызывает:
            AppExceptionResponse.unauthorized: Если токен недействителен или истек.
            AppExceptionResponse.bad_request: Если пользователь не найден или неактивен.
        """
        # Проверяем и декодируем refresh token
        user_data = self._verify_refresh_token(refresh_token)

        # Проверяем срок действия
        expire = user_data.get("exp")
        if not expire or int(expire) < datetime.now().timestamp():
            raise AppExceptionResponse.unauthorized(
                message=i18n.gettext("token_expired")
            )

        # Получаем ID пользователя
        user_id = user_data.get("sub")
        if not user_id:
            raise AppExceptionResponse.unauthorized(
                message=i18n.gettext("user_not_found")
            )

        # Проверяем существование и активность пользователя
        user = await self.repository.get(id=int(user_id))
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        if not user.is_active:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_active")
            )

        # Создаем новые токены
        new_access_token = create_access_token(data=user.id)
        new_refresh_token = create_refresh_token(data=user.id)

        return BearerTokenDTO(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    async def validate(self) -> None:
        """
        Заглушка для потенциальной логики валидации.
        """
        pass

    def _verify_refresh_token(self, token: str) -> dict:
        """
        Проверяет и декодирует refresh token.

        Аргументы:
            token (str): Refresh token для проверки.

        Возвращает:
            dict: Расшифрованные данные токена.

        Вызывает:
            AppExceptionResponse.unauthorized: Если токен недействителен.
            AppExceptionResponse.forbidden: Если токен не является refresh token.
        """
        try:
            decoded_data = jwt.decode(
                token, app_config.secret_key, algorithms=app_config.algorithm
            )
            if decoded_data.get("type") != "refresh":
                raise AppExceptionResponse.forbidden(
                    message=i18n.gettext("invalid_token_type")
                )
        except jwt.JWTError as jwt_error:
            raise AppExceptionResponse.unauthorized(
                message=f"Error: {jwt_error!s}"
            ) from jwt_error
        else:
            return decoded_data