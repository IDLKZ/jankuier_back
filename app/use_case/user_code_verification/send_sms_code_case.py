import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationResultRDTO,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_code_verification_entity import UserCodeVerificationEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.smsc.smsc_api import SMSC
from app.use_case.base_case import BaseUseCase


class SendSmsCodeCase(BaseUseCase[UserCodeVerificationResultRDTO]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_code_verification_repository = UserCodeVerificationRepository(db)

    async def execute(self, phone: str) -> UserCodeVerificationResultRDTO:
        await self.validate(phone=phone)
        code = await self.transform(phone=phone)

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

        # Calculate expiration time
        expire_time = datetime.utcnow() + timedelta(minutes=app_config.sms_code_expire_minutes)
        expires_in_seconds = app_config.sms_code_expire_minutes * 60

        # Create verification record
        verification_entity = UserCodeVerificationEntity(
            user_id=user.id,
            code=code,
            expired_at=expire_time
        )

        await self.user_code_verification_repository.create(verification_entity)

        # Send SMS
        message = None
        result = False

        try:
            if app_config.use_sms_service:
                # Use real SMS service
                smsc = SMSC()
                sms_message = (
                    f"{i18n.gettext('sms_verification_code_message').format(code=code)}\n"
                    f"{i18n.gettext('sms_verification_code_message_kk').format(code=code)}"
                )

                sms_result = smsc.send_sms(
                    user.phone,
                    sms_message,
                    sender="sms"
                )

                # Check if SMS was sent successfully
                if len(sms_result) >= 2 and int(sms_result[1]) > 0:
                    result = True
                    message = i18n.gettext("sms_sent_successfully")
                else:
                    message = i18n.gettext("sms_sending_failed")
            else:
                # Use fake SMS service
                result = True
                message = i18n.gettext("sms_sent_successfully")

        except Exception as e:
            message = i18n.gettext("sms_sending_error")

        return UserCodeVerificationResultRDTO(
            user_id=user.id,
            phone=user.phone,
            result=result,
            expires_in_seconds=expires_in_seconds,
            message=message
        )

    async def validate(self, phone: str) -> None:
        # Check if phone is provided
        if not phone or len(phone.strip()) == 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("phone_required")
            )

        # Get user by phone number
        user = await self.user_repository.get_first_with_filters(
            filters=[
                self.user_repository.model.phone == phone
            ]
        )
        if not user:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("user_not_found")
            )

        # Check if user is registered
        if not user.is_active:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_active")
            )

        # Check if user is already verified
        if user.is_verified:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_already_verified")
            )

    async def transform(self, phone: str) -> str:
        # Generate 4-digit code if using real SMS service
        if app_config.use_sms_service:
            return f"{random.randint(0, 9999):04d}"
        else:
            return app_config.fake_sms_code