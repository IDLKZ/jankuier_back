from pydantic import BaseModel

from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant


class UserCodeResetPasswordDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class UserCodeResetPasswordCDTO(BaseModel):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    expired_at: DTOConstant.StandardDateTimeField(description="Время истечения кода")
    code: DTOConstant.StandardVarcharField(description="Код сброса пароля")

    class Config:
        from_attributes = True


class UserCodeResetPasswordRDTO(UserCodeResetPasswordDTO):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    expired_at: DTOConstant.StandardDateTimeField(description="Время истечения кода")
    code: DTOConstant.StandardVarcharField(description="Код сброса пароля")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class UserCodeResetPasswordWithRelationsRDTO(UserCodeResetPasswordRDTO):
    user: UserRDTO | None = None

    class Config:
        from_attributes = True


class UserCodeResetPasswordConfirm(BaseModel):
    code: DTOConstant.StandardVarcharField(description="Код сброса пароля")
    phone: DTOConstant.StandardPhoneField(description="Код сброса пароля")
    new_password:DTOConstant.StandardPasswordField(description="Новый пароль")
