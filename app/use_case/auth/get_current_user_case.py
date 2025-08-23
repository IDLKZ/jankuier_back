from datetime import datetime

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.role.role_repository import RoleRepository
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO


class GetCurrentUserCase(BaseUseCase[UserWithRelationsRDTO]):
    """
    Получение текущего пользователя по токену.

    - Если используется Keycloak, проверяет `userinfo`.
    - Если используется локальная аутентификация, декодирует `JWT`.
    - Если пользователь отсутствует в БД, создаёт его.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация зависимостей для работы с пользователем.

        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    async def execute(self, token: str) -> UserWithRelationsRDTO:
        """
        Выполняет проверку и получение текущего пользователя.

        1. Проверяет, используется ли Keycloak.
        2. Если да, получает `userinfo` и преобразует его в DTO.
        3. Проверяет наличие пользователя в БД, обновляет или создаёт его.
        4. Если Keycloak не используется, проверяет локальный `JWT` и ищет пользователя по `user_id`.

        :param token: JWT-токен пользователя.
        :return: DTO с данными пользователя.
        """
        return await self._handle_local_auth(token)

    async def _handle_local_auth(self, token: str) -> UserWithRelationsRDTO:
        """
        Обрабатывает локальную аутентификацию (без Keycloak).

        :param token: JWT-токен пользователя.
        :return: DTO с пользователем.
        """
        user_data: dict = self.local_verify_jwt_token(token)
        expire = user_data.get("exp")

        if not expire or int(expire) < datetime.now().timestamp():
            raise AppExceptionResponse.unauthorized(
                message=i18n.gettext("token_expired")
            )

        user_id = int(user_data.get("sub"))
        if not user_id:
            raise AppExceptionResponse.unauthorized(
                message=i18n.gettext("user_not_found")
            )

        user = await self.repository.get(
            id=user_id, options=self.repository.default_relationships()
        )
        return UserWithRelationsRDTO.from_orm(user)

    async def validate(self) -> None:
        pass

    def local_verify_jwt_token(self, token: str) -> dict:
        """
        Локальная проверка `JWT`.

        :param token: JWT-токен.
        :return: Расшифрованные данные токена.
        """
        try:
            decoded_data = jwt.decode(
                token, app_config.secret_key, algorithms=app_config.algorithm
            )
            if decoded_data.get("type") != "access":
                raise AppExceptionResponse.forbidden(message=i18n.gettext("forbidden"))
        except jwt.JWTError as jwtError:
            raise AppExceptionResponse.unauthorized(
                message=f"Error: {jwtError!s}"
            ) from jwtError
        else:
            return decoded_data
