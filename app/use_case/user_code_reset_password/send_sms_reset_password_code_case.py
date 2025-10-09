import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeResetPasswordResultRDTO,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.adapters.repository.user_code_reset_password_repository import (
    UserCodeResetPasswordRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.smsc.smsc_api import SMSC
from app.use_case.base_case import BaseUseCase


class SendSmsResetPasswordCodeCase(BaseUseCase[UserCodeResetPasswordResultRDTO]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_code_reset_password_repository = UserCodeResetPasswordRepository(db)

    async def execute(self, phone: str) -> UserCodeResetPasswordResultRDTO:
        await self.validate(phone=phone)

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

        # Check if there's an active reset code
        active_reset_code = await self.user_code_reset_password_repository.get_first_with_filters(
            filters=[
                self.user_code_reset_password_repository.model.user_id == user.id,
                self.user_code_reset_password_repository.model.expired_at > datetime.utcnow()
            ],
            order_by="created_at",
            order_direction="DESC"
        )

        if active_reset_code:
            # Use existing active code
            code = active_reset_code.code
            expire_time = active_reset_code.expired_at
            expires_in_seconds = int((expire_time - datetime.utcnow()).total_seconds())
        else:
            # Generate new code
            code = await self.transform(phone=phone)

            # Calculate expiration time
            expire_time = datetime.utcnow() + timedelta(minutes=app_config.sms_code_expire_minutes)
            expires_in_seconds = app_config.sms_code_expire_minutes * 60

            # Create reset password code record
            reset_code_entity = UserCodeResetPasswordEntity(
                user_id=user.id,
                code=code,
                expired_at=expire_time
            )

            await self.user_code_reset_password_repository.create(reset_code_entity)

        # Send SMS
        message = None
        result = False

        try:
            if app_config.use_sms_service:
                # Use real SMS service
                smsc = SMSC()
                sms_message = (
                    f"Для сброса пароля введите следующий код: {code}. Никому не сообщайте код."
                    f"Құпия сөзді қалпына келтіру үшін сіздің кодыңыз: {code}. Кодты ешкімге айтпаңыз."
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

        return UserCodeResetPasswordResultRDTO(
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
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Check if user is active
        if not user.is_active:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_active")
            )

    async def transform(self, phone: str) -> str:
        # Generate 4-digit code if using real SMS service
        if app_config.use_sms_service:
            return f"{random.randint(0, 9999):04d}"
        else:
            return app_config.fake_sms_code
