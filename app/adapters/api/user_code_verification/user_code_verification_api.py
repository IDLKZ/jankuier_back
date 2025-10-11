from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.adapters.dto.pagination_dto import PaginationUserCodeVerificationRDTO, \
    PaginationUserCodeVerificationWithRelationsRDTO
from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationCDTO,
    UserCodeVerificationUDTO,
    UserCodeVerificationWithRelationsRDTO,
    UserCodeVerificationResultRDTO,
)
from app.adapters.filters.user_code_verification.user_code_verification_filter import (
    UserCodeVerificationFilter,
    UserCodeVerificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.dto_constants import DTOConstant
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.user_code_verification.all_user_code_verification_case import (
    AllUserCodeVerificationCase,
)
from app.use_case.user_code_verification.create_user_code_verification_case import (
    CreateUserCodeVerificationCase,
)
from app.use_case.user_code_verification.delete_user_code_verification_case import (
    DeleteUserCodeVerificationCase,
)
from app.use_case.user_code_verification.get_user_code_verification_by_id_case import (
    GetUserCodeVerificationByIdCase,
)
from app.use_case.user_code_verification.paginate_user_code_verification_case import (
    PaginateUserCodeVerificationCase,
)
from app.use_case.user_code_verification.send_sms_code_case import SendSmsCodeCase
from app.use_case.user_code_verification.update_user_code_verification_case import (
    UpdateUserCodeVerificationCase,
)
from app.use_case.user_code_verification.verify_sms_code_case import VerifySmsCodeCase


class SendSmsCodeDTO(BaseModel):
    phone: DTOConstant.StandardPhoneField(description="Номер телефона пользователя")


class VerifySmsCodeDTO(BaseModel):
    phone: DTOConstant.StandardPhoneField(description="Номер телефона пользователя")
    code: DTOConstant.StandardVarcharField(description="Код подтверждения")


class UserCodeVerificationApi:
    def __init__(self):
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        # Standard CRUD routes
        self.router.add_api_route(
            RoutePathConstants.IndexPathName,
            self.index,
            methods=["GET"],
            response_model=PaginationUserCodeVerificationWithRelationsRDTO,
            summary="Получить список кодов верификации (пагинация)",
            description="Возвращает пагинированный список кодов верификации пользователей",
        )

        self.router.add_api_route(
            RoutePathConstants.AllPathName,
            self.all,
            methods=["GET"],
            response_model=list[UserCodeVerificationWithRelationsRDTO],
            summary="Получить все коды верификации",
            description="Возвращает полный список кодов верификации без пагинации",
        )

        self.router.add_api_route(
            RoutePathConstants.CreatePathName,
            self.create,
            methods=["POST"],
            response_model=UserCodeVerificationWithRelationsRDTO,
            summary="Создать код верификации",
            description="Создает новый код верификации для пользователя",
        )

        self.router.add_api_route(
            RoutePathConstants.UpdatePathName,
            self.update,
            methods=["PUT"],
            response_model=UserCodeVerificationWithRelationsRDTO,
            summary="Обновить код верификации",
            description="Обновляет существующий код верификации",
        )

        self.router.add_api_route(
            RoutePathConstants.GetByIdPathName,
            self.get,
            methods=["GET"],
            response_model=UserCodeVerificationWithRelationsRDTO,
            summary="Получить код верификации по ID",
            description="Возвращает код верификации по его уникальному идентификатору",
        )

        self.router.add_api_route(
            RoutePathConstants.DeleteByIdPathName,
            self.delete,
            methods=["DELETE"],
            response_model=bool,
            summary="Удалить код верификации",
            description="Удаляет код верификации по ID (soft delete по умолчанию)",
        )

        # Special SMS routes
        self.router.add_api_route(
            "/send-code",
            self.send_sms_code,
            methods=["POST"],
            response_model=UserCodeVerificationResultRDTO,
            summary="Отправить SMS код",
            description="Отправляет SMS код подтверждения на указанный номер телефона",
        )

        self.router.add_api_route(
            "/verify-code",
            self.verify_sms_code,
            methods=["POST"],
            response_model=UserCodeVerificationResultRDTO,
            summary="Проверить SMS код",
            description="Проверяет SMS код подтверждения и верифицирует пользователя",
        )

    async def index(
        self,
        filter_params: UserCodeVerificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationUserCodeVerificationWithRelationsRDTO:
        """Получить пагинированный список кодов верификации"""
        try:
            return await PaginateUserCodeVerificationCase(db).execute(
                filter_params=filter_params
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def all(
        self,
        filter_params: UserCodeVerificationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[UserCodeVerificationWithRelationsRDTO]:
        """Получить все коды верификации"""
        try:
            return await AllUserCodeVerificationCase(db).execute(
                filter_params=filter_params
            )
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
        dto: UserCodeVerificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Создать код верификации"""
        try:
            return await CreateUserCodeVerificationCase(db).execute(dto=dto)
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
        dto: UserCodeVerificationUDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Обновить код верификации"""
        try:
            return await UpdateUserCodeVerificationCase(db).execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Получить код верификации по ID"""
        try:
            return await GetUserCodeVerificationByIdCase(db).execute(
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

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """Удалить код верификации"""
        try:
            return await DeleteUserCodeVerificationCase(db).execute(
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

    async def send_sms_code(
        self,
        dto: SendSmsCodeDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationResultRDTO:
        """Отправить SMS код"""
        return await SendSmsCodeCase(db).execute(phone=dto.phone)

    async def verify_sms_code(
        self,
        dto: VerifySmsCodeDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationResultRDTO:
        """Проверить SMS код"""
        return await VerifySmsCodeCase(db).execute(phone=dto.phone, code=dto.code)