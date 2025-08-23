from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.auth.login_dto import LoginDTO
from app.adapters.dto.auth.register_dto import RegisterDTO
from app.adapters.dto.auth.token_dto import BearerTokenDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.auth.login_case import LoginCase
from app.use_case.auth.register_case import RegisterCase


class AuthApi:

    def __init__(self) -> None:
        """
        Инициализация AuthApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API авторизацией.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """
        Регистрация маршрутов API для аутентификации.
        Маршруты включают:
            - POST /login: Авторизация пользователя.
            - GET /me: Получение данных авторизованного пользователя.
        """
        self.router.post(
            f"{RoutePathConstants.LoginPathName}",
            response_model=BearerTokenDTO,
            summary="Авторизация",
            description="Авторизуйтесь с помощью username и password",
        )(self.sign_in)
        self.router.post(
            f"{RoutePathConstants.RegisterPathName}",
            response_model=UserWithRelationsRDTO,
            summary="Регистрация",
            description="Регистрация пользователя",
        )(self.sign_up)
        self.router.post(
            f"{RoutePathConstants.LoginSwaggerPathName}",
            response_model=BearerTokenDTO,
            summary="Авторизация",
            description="Авторизуйтесь с помощью username и password",
        )(self.sign_in_swagger)
        self.router.get(
            f"{RoutePathConstants.GetMePathName}",
            response_model=UserWithRelationsRDTO,
            summary="Получить авторизованного пользователя",
            description="Данные пользователя",
        )(self.me)

    async def sign_in(
        self, dto: LoginDTO, db: AsyncSession = Depends(get_db)
    ) -> BearerTokenDTO:
        """
        Выполняет авторизацию пользователя.
        Args:
            dto (LoginDTO): Данные для авторизации, включая username и password.
            db (AsyncSession): Сессия базы данных.
        Returns:
            BearerTokenDTO: Токен доступа.
        Raises:
            HTTPException: При ошибках аутентификации.
            AppExceptionResponse: При внутренних ошибках.
        """
        use_case = LoginCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def sign_up(
        self, dto: RegisterDTO, db: AsyncSession = Depends(get_db)
    ) -> BearerTokenDTO:
        """
        Выполняет авторизацию пользователя.
        Args:
            dto (LoginDTO): Данные для авторизации, включая username и password.
            db (AsyncSession): Сессия базы данных.
        Returns:
            BearerTokenDTO: Токен доступа.
        Raises:
            HTTPException: При ошибках аутентификации.
            AppExceptionResponse: При внутренних ошибках.
        """
        use_case = RegisterCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при регистрации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def me(
        self, user: UserWithRelationsRDTO = Depends(get_current_user)
    ) -> UserWithRelationsRDTO:
        """
        Возвращает данные текущего авторизованного пользователя.
        Args:
            user (UserWithRelationsRDTO): Данные авторизованного пользователя.
        Returns:
            UserWithRelationsRDTO: Данные пользователя.
        Raises:
            HTTPException: При ошибках получения данных.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return user
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def sign_in_swagger(
        self,
        uform_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> BearerTokenDTO:
        """
        Выполняет авторизацию пользователя.
        Args:
            dto (LoginDTO): Данные для авторизации, включая username и password.
            db (AsyncSession): Сессия базы данных.
        Returns:
            BearerTokenDTO: Токен доступа.
        Raises:
            HTTPException: При ошибках аутентификации.
            AppExceptionResponse: При внутренних ошибках.
        """
        use_case = LoginCase(db)
        try:
            dto = LoginDTO(username=uform_data.username, password=uform_data.password)
            result = await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"id": id, "details": str(exc)},
                is_custom=True,
            ) from exc

        else:
            return {"access_token": result.access_token, "token_type": "bearer"}
