import traceback

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.auth.login_dto import LoginDTO
from app.adapters.dto.auth.refresh_token_dto import RefreshTokenDTO
from app.adapters.dto.auth.register_dto import RegisterDTO, UpdateProfileDTO, UpdatePasswordDTO
from app.adapters.dto.auth.token_dto import BearerTokenDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import get_current_user
from app.helpers.form_helper import FormParserHelper
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.middleware.role_middleware import check_client
from app.shared.route_constants import RoutePathConstants
from app.use_case.auth.deactivate_my_account import DeactivateMyAccount
from app.use_case.auth.login_case import LoginCase
from app.use_case.auth.login_client_case import LoginClientCase
from app.use_case.auth.refresh_token_case import RefreshTokenCase
from app.use_case.auth.register_case import RegisterCase
from app.use_case.auth.update_profile_case import UpdateProfileCase
from app.use_case.auth.update_password_case import UpdatePasswordCase
from app.use_case.auth.update_profile_photo_case import UpdateProfilePhotoCase


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
            f"{RoutePathConstants.LoginPathName}-client",
            response_model=BearerTokenDTO,
            summary="Авторизация",
            description="Авторизуйтесь с помощью username и password",
        )(self.sign_in_client)
        self.router.post(
            f"{RoutePathConstants.RegisterPathName}",
            response_model=UserWithRelationsRDTO,
            summary="Регистрация",
            description="Регистрация пользователя",
        )(self.sign_up)
        self.router.post(
            f"{RoutePathConstants.RefreshTokenPathName}",
            response_model=BearerTokenDTO,
            summary="Обновление токенов",
            description="Обновление токенов доступа с помощью refresh token",
        )(self.refresh_token)
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
        self.router.post(
            f"{RoutePathConstants.UpdateProfilePathName}",
            response_model=UserWithRelationsRDTO,
            summary="Обновить профиль",
            description="Обновление данных профиля пользователя",
        )(self.update_profile)
        self.router.post(
            f"{RoutePathConstants.UpdatePasswordPathName}",
            response_model=bool,
            summary="Изменить пароль",
            description="Изменение пароля пользователя",
        )(self.update_password)
        self.router.put(
            f"{RoutePathConstants.UpdateProfilePhotoPathName}",
            response_model=UserWithRelationsRDTO,
            summary="Обновить фото профиля",
            description="Загрузка или обновление фото профиля пользователя",
        )(self.update_profile_photo)
        self.router.delete(
            f"{RoutePathConstants.DeleteProfilePhotoPathName}",
            response_model=UserWithRelationsRDTO,
            summary="Удалить фото профиля",
            description="Удаление фото профиля пользователя",
        )(self.delete_profile_photo)
        self.router.delete(
            f"/deactivate-my-account",
            response_model=bool,
            summary="Деактивировать аккаунт",
            description="Деактивировать аккаунт",
        )(self.deactivate)

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
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def sign_in_client(
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
        use_case = LoginClientCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message="Ошибка при логинации",
                extra={"details": str(exc)},
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
                extra={"details": str(exc)},
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
                extra={"details": str(exc)},
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
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

        else:
            return {"access_token": result.access_token, "token_type": "bearer"}

    async def update_profile(
        self,
        dto: UpdateProfileDTO,
        user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        """
        Обновляет профиль пользователя.
        Args:
            dto (UpdateProfileDTO): Данные для обновления профиля.
            user (UserWithRelationsRDTO): Текущий авторизованный пользователь.
            db (AsyncSession): Сессия базы данных.
        Returns:
            UserWithRelationsRDTO: Обновленные данные пользователя.
        Raises:
            HTTPException: При ошибках обновления профиля.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return await UpdateProfileCase(db).execute(user_id=user.id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"user_id": user.id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def update_password(
        self,
        dto: UpdatePasswordDTO,
        user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Изменяет пароль пользователя.
        Args:
            dto (UpdatePasswordDTO): Данные для смены пароля.
            user (UserWithRelationsRDTO): Текущий авторизованный пользователь.
            db (AsyncSession): Сессия базы данных.
        Returns:
            bool: True если пароль успешно изменен.
        Raises:
            HTTPException: При ошибках смены пароля.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return await UpdatePasswordCase(db).execute(user_id=user.id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"user_id": user.id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def update_profile_photo(
        self,
        file: UploadFile = File(..., description="Фото профиля"),
        user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        """
        Обновляет фото профиля пользователя.
        Args:
            file (UploadFile): Файл изображения.
            user (UserWithRelationsRDTO): Текущий авторизованный пользователь.
            db (AsyncSession): Сессия базы данных.
        Returns:
            UserWithRelationsRDTO: Обновленные данные пользователя.
        Raises:
            HTTPException: При ошибках загрузки фото.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return await UpdateProfilePhotoCase(db).execute(user_id=user.id, file=file)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"user_id": user.id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete_profile_photo(
        self,
        user: UserWithRelationsRDTO = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        """
        Удаляет фото профиля пользователя.
        Args:
            user (UserWithRelationsRDTO): Текущий авторизованный пользователь.
            db (AsyncSession): Сессия базы данных.
        Returns:
            UserWithRelationsRDTO: Обновленные данные пользователя.
        Raises:
            HTTPException: При ошибках удаления фото.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return await UpdateProfilePhotoCase(db).delete_photo(user_id=user.id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"user_id": user.id, "details": str(exc)},
                is_custom=True,
            ) from exc

    async def refresh_token(
        self, dto: RefreshTokenDTO, db: AsyncSession = Depends(get_db)
    ) -> BearerTokenDTO:
        """
        Обновляет токены доступа с помощью refresh token.
        Args:
            dto (RefreshTokenDTO): Данные с refresh token.
            db (AsyncSession): Сессия базы данных.
        Returns:
            BearerTokenDTO: Новые токены доступа.
        Raises:
            HTTPException: При ошибках обновления токенов.
            AppExceptionResponse: При внутренних ошибках.
        """
        try:
            return await RefreshTokenCase(db).execute(refresh_token=dto.refresh_token)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def deactivate(
        self,
        user:UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        use_case = DeactivateMyAccount(db)
        try:
            return await use_case.execute(id=user.id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc
