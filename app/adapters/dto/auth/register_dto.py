from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class RegisterDTO(BaseModel):
    role_id: DTOConstant.StandardNullableIntegerField(description="ID роли")
    email: DTOConstant.StandardEmailField(description="Email")
    phone: DTOConstant.StandardPhoneField(description="Телефон")
    username: DTOConstant.StandardLoginField(description="Логин")
    iin: DTOConstant.StandardNullableIINField(description="ИИН")
    password: DTOConstant.StandardPasswordField()
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronymic: DTOConstant.StandardNullableVarcharField(description="Отчество")

    class Config:
        from_attributes = True


class UpdateProfileDTO(BaseModel):
    email: DTOConstant.StandardEmailField(description="Email")
    phone: DTOConstant.StandardPhoneField(description="Телефон")
    iin: DTOConstant.StandardNullableIINField(description="ИИН")
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronymic: DTOConstant.StandardNullableVarcharField(description="Отчество")

    class Config:
        from_attributes = True

class UpdatePasswordDTO(BaseModel):
    old_password: DTOConstant.StandardPasswordField(description="Старый пароль")
    new_password: DTOConstant.StandardPasswordField(description="Новый пароль")