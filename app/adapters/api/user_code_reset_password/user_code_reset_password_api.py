from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_reset_password.user_code_reset_password_dto import (
    UserCodeResetPasswordCDTO,
    UserCodeResetPasswordWithRelationsRDTO,
    PaginationUserCodeResetPasswordRDTO, UserCodeResetPasswordConfirm,
)
from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeResetPasswordResultRDTO,
)
from app.adapters.filters.user_code_reset_password.user_code_reset_password_filter import (
    UserCodeResetPasswordFilter,
)
from app.adapters.filters.user_code_reset_password.user_code_reset_password_pagination_filter import (
    UserCodeResetPasswordPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.user_code_reset_password.all_user_code_reset_password_case import (
    AllUserCodeResetPasswordCase,
)
from app.use_case.user_code_reset_password.create_user_code_reset_password_case import (
    CreateUserCodeResetPasswordCase,
)
from app.use_case.user_code_reset_password.delete_user_code_reset_password_case import (
    DeleteUserCodeResetPasswordCase,
)
from app.use_case.user_code_reset_password.get_user_code_reset_password_by_id_case import (
    GetUserCodeResetPasswordByIdCase,
)
from app.use_case.user_code_reset_password.paginate_user_code_reset_password_case import (
    PaginateUserCodeResetPasswordCase,
)
from app.use_case.user_code_reset_password.update_user_code_reset_password_case import (
    UpdateUserCodeResetPasswordCase,
)
from app.use_case.user_code_reset_password.send_sms_reset_password_code_case import (
    SendSmsResetPasswordCodeCase,
)
from app.use_case.user_code_reset_password.verify_sms_reset_code_case import VerifySmsResetCodeCase


class UserCodeResetPasswordApi:
    def __init__(self) -> None:
        """
        Инициализация UserCodeResetPasswordApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API кодов сброса пароля.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationUserCodeResetPasswordRDTO,
            summary="Список кодов сброса пароля с пагинацией",
            description="Получение списка кодов сброса пароля с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[UserCodeResetPasswordWithRelationsRDTO],
            summary="Список всех кодов сброса пароля",
            description="Получение полного списка кодов сброса пароля",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=UserCodeResetPasswordWithRelationsRDTO,
            summary="Создать код сброса пароля",
            description="Создание нового кода сброса пароля",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=UserCodeResetPasswordWithRelationsRDTO,
            summary="Обновить код сброса пароля по ID",
            description="Обновление информации о коде сброса пароля по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=UserCodeResetPasswordWithRelationsRDTO,
            summary="Получить код сброса пароля по ID",
            description="Получение информации о коде сброса пароля по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить код сброса пароля по ID",
            description="Удаление кода сброса пароля по ID",
        )(self.delete)

        self.router.post(
            "/send-sms-reset-password-code",
            response_model=UserCodeResetPasswordResultRDTO,
            summary="Отправить SMS код для сброса пароля",
            description="Отправка SMS кода для сброса пароля на номер телефона пользователя",
        )(self.send_sms_reset_password_code)

        self.router.post(
            "/verify-sms-reset-password-code",
            response_model=UserCodeResetPasswordResultRDTO,
            summary="Отправить SMS код для сброса пароля",
            description="Отправка SMS кода для сброса пароля на номер телефона пользователя",
        )(self.verify_sms_reset_password_code)

    async def paginate(
        self,
        filter: UserCodeResetPasswordPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationUserCodeResetPasswordRDTO:
        try:
            return await PaginateUserCodeResetPasswordCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: UserCodeResetPasswordFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[UserCodeResetPasswordWithRelationsRDTO]:
        try:
            return await AllUserCodeResetPasswordCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: UserCodeResetPasswordCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeResetPasswordWithRelationsRDTO:
        try:
            return await CreateUserCodeResetPasswordCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: UserCodeResetPasswordCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeResetPasswordWithRelationsRDTO:
        try:
            return await UpdateUserCodeResetPasswordCase(db).execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeResetPasswordWithRelationsRDTO:
        try:
            return await GetUserCodeResetPasswordByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        try:
            return await DeleteUserCodeResetPasswordCase(db).execute(
                id=id, force_delete=force_delete
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def send_sms_reset_password_code(
        self,
        phone: str,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeResetPasswordResultRDTO:
        """
        Отправляет SMS код для сброса пароля.

        Args:
            phone: Номер телефона пользователя
            db: Сессия базы данных

        Returns:
            UserCodeResetPasswordResultRDTO: Результат отправки SMS
        """
        try:
            return await SendSmsResetPasswordCodeCase(db).execute(phone=phone)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc


    async def verify_sms_reset_password_code(
        self,
        dto: UserCodeResetPasswordConfirm,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeResetPasswordResultRDTO:
        """
        Отправляет SMS код для сброса пароля.

        Args:
            phone: Номер телефона пользователя
            db: Сессия базы данных

        Returns:
            UserCodeResetPasswordResultRDTO: Результат отправки SMS
        """
        try:
            return await VerifySmsResetCodeCase(db).execute(phone=dto.phone, new_password=dto.new_password, code=dto.code)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
