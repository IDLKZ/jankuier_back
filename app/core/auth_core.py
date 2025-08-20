from datetime import datetime, timedelta
from typing import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from packaging.utils import _
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.relation_dto.user_relation import LocalUserWithRelationsDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.auth.get_current_user_case import GetCurrentUserCase

# Утилиты и конфигурации
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{RoutePathConstants.BasePathName}{RoutePathConstants.AuthPathName}{RoutePathConstants.LoginSwaggerPathName}"
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Хэширование и проверка паролей ===
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# === Работа с токенами ===
def create_access_token(data: int) -> str:
    """Создает Access Token."""
    to_encode = {"sub": str(data), "type": "access"}
    expire = datetime.now() + timedelta(minutes=app_config.access_token_expire_minutes)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, app_config.secret_key, algorithm=app_config.algorithm)


def create_refresh_token(data: int) -> str:
    """Создает Refresh Token."""
    to_encode = {"sub": str(data), "type": "refresh"}
    expire = datetime.now() + timedelta(days=app_config.refresh_token_expire_days)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, app_config.secret_key, algorithm=app_config.algorithm)


# === Получение текущего пользователя ===
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> LocalUserWithRelationsDTO:
    use_case = GetCurrentUserCase(db)
    user = await use_case.execute(token)
    if not user:
        raise AppExceptionResponse.unauthorized(message="Не авторизован")
    return user


def role_checker(required_roles: list[str]) -> Callable:
    def checker(current_user: UserWithRelationsRDTO = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise AppExceptionResponse.forbidden(
                message=_("forbidden"),
            )
        return current_user

    return checker


def check_authorized_user() -> Callable:
    def checker(current_user: UserWithRelationsRDTO = Depends(get_current_user)):
        if not current_user:
            raise AppExceptionResponse.unauthorized(
                message="Не авторизирован",
            )
        return current_user

    return checker
