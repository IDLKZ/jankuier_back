from pydantic import BaseModel

from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class UserCodeVerificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class UserCodeVerificationCDTO(BaseModel):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    expired_at: DTOConstant.StandardDateTimeField(description="Время истечения кода")
    code: DTOConstant.StandardVarcharField(description="Код подтверждения")

    class Config:
        from_attributes = True


class UserCodeVerificationRDTO(UserCodeVerificationDTO):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    expired_at: DTOConstant.StandardDateTimeField(description="Время истечения кода")
    code: DTOConstant.StandardVarcharField(description="Код подтверждения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class UserCodeVerificationWithRelationsRDTO(UserCodeVerificationRDTO):
    user: UserRDTO | None = None

    class Config:
        from_attributes = True

class UserCodeVerificationResultRDTO(BaseModel):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    phone: DTOConstant.StandardVarcharField(description="Номер пользователя")
    result: DTOConstant.StandardBooleanFalseField(description="Результат")
    expires_in_seconds: DTOConstant.StandardUnsignedIntegerField(description="Время истечения кода")
    message: DTOConstant.StandardNullableTextField(description="Сообщение")
