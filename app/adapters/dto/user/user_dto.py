from pydantic import BaseModel

from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.role.role_dto import RoleRDTO
from app.shared.dto_constants import DTOConstant


class UserDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class UserCDTO(BaseModel):
    role_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID роли")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения"
    )
    # region_id: DTOConstant.StandardNullableUnsignedIntegerField(
    #     description="ID региона"
    # )

    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronomic: DTOConstant.StandardNullableVarcharField(description="Отчество")

    email: DTOConstant.StandardEmailField(description="Электронная почта")
    phone: DTOConstant.StandardPhoneField(description="Телефон")
    username: DTOConstant.StandardUniqueValueField(
        description="Уникальное имя пользователя"
    )
    sex: DTOConstant.StandardNullableIntegerField(
        description="Пол (0 - не указан, 1 - мужской, 2 - женский)"
    )

    iin: DTOConstant.StandardNullableVarcharField(description="ИИН")
    birthdate: DTOConstant.StandardNullableDateTimeField(description="Дата рождения")

    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_verified: DTOConstant.StandardBooleanFalseField(description="Подтвержден")

    password_hash: DTOConstant.StandardPasswordField(description="Password")

    class Config:
        from_attributes = True


class UserRDTO(UserDTO):
    role_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID роли")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения"
    )
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronomic: DTOConstant.StandardNullableVarcharField(description="Отчество")

    email: DTOConstant.StandardEmailField(description="Электронная почта")
    phone: DTOConstant.StandardVarcharField(description="Телефон")
    username: DTOConstant.StandardUniqueValueField(
        description="Уникальное имя пользователя"
    )
    sex: DTOConstant.StandardNullableIntegerField(description="Пол")

    iin: DTOConstant.StandardNullableVarcharField(description="ИИН")
    birthdate: DTOConstant.StandardNullableDateTimeField(description="Дата рождения")

    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_verified: DTOConstant.StandardBooleanFalseField(description="Подтвержден")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class UserWithRelationsRDTO(UserRDTO):
    role: RoleRDTO | None = None
    image: FileRDTO | None = None

    class Config:
        from_attributes = True
