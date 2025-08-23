from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class RegisterDTO(BaseModel):
    role_id: DTOConstant.StandardIntegerField(description="ID роли")
    email: DTOConstant.StandardEmailField(description="Email")
    phone: DTOConstant.StandardPhoneField(description="Телефон")
    username: DTOConstant.StandardLoginField(description="Логин")
    iin: DTOConstant.StandardUniqueIINField(description="ИИН")
    password: DTOConstant.StandardPasswordField()
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronymic: DTOConstant.StandardNullableVarcharField(description="Отчество")

    class Config:
        from_attributes = True
