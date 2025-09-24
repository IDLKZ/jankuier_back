from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationResultRDTO,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config

from app.use_case.base_case import BaseUseCase


class VerifySmsCodeCase(BaseUseCase[UserCodeVerificationResultRDTO]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_code_verification_repository = UserCodeVerificationRepository(db)

    async def execute(self, phone: str, code: str) -> UserCodeVerificationResultRDTO:
        await self.validate(phone=phone, code=code)

        # Get user by phone number
        user = await self.user_repository.get_first_with_filters(
            filters=[
                self.user_repository.model.phone == phone
            ]
        )
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Get the most recent verification code
        verification = await self.user_code_verification_repository.get_first_with_filters(
            filters=[
                self.user_code_verification_repository.model.user_id == user.id
            ],
            order_by="created_at",
            order_direction="desc"
        )

        result = False
        message = None
        expires_in_seconds = 0

        if verification:
            # Calculate expiration time based on created_at + sms_code_verify_minutes
            now = datetime.utcnow()
            expiration_time = verification.created_at + timedelta(minutes=app_config.sms_code_verify_minutes)

            if expiration_time > now:
                expires_in_seconds = int((expiration_time - now).total_seconds())

                # Check if code matches
                expected_code = app_config.fake_sms_code if not app_config.use_sms_service else verification.code

                if code == expected_code:
                    # Mark user as verified
                    await self.user_repository.update(user, {"is_verified": True})
                    result = True
                    message = i18n.gettext("code_verified_successfully")
                else:
                    message = i18n.gettext("invalid_verification_code")
            else:
                message = i18n.gettext("verification_code_expired")
        else:
            message = i18n.gettext("no_verification_code_found")

        return UserCodeVerificationResultRDTO(
            user_id=user.id,
            phone=user.phone,
            result=result,
            expires_in_seconds=expires_in_seconds,
            message=message
        )

    async def validate(self, phone: str, code: str) -> None:
        # Check if phone is provided
        if not phone or len(phone.strip()) == 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("phone_required")
            )

        # Check if code is provided
        if not code or len(code.strip()) == 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("verification_code_required")
            )

        # Check if user exists
        user = await self.user_repository.get_first_with_filters(
            filters=[
                self.user_repository.model.phone == phone
            ]
        )
        if not user:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("user_not_found")
            )

    async def transform(self, **kwargs) -> None:
        # No transformation needed for this use case
        pass