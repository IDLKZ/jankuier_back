from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationResultRDTO,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.dto_constants import DTOConstant
from app.shared.route_constants import RoutePathConstants
from app.use_case.user_code_verification.send_sms_code_case import SendSmsCodeCase
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

    async def send_sms_code(
        self,
        dto: SendSmsCodeDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationResultRDTO:
        try:
            return await SendSmsCodeCase(db).execute(phone=dto.phone)
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def verify_sms_code(
        self,
        dto: VerifySmsCodeDTO,
        db: AsyncSession = Depends(get_db),
    ) -> UserCodeVerificationResultRDTO:
        try:
            return await VerifySmsCodeCase(db).execute(phone=dto.phone, code=dto.code)
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc