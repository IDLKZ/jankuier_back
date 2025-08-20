from pydantic import BaseModel

from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.shared.dto_constants import DTOConstant


class RoleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class RoleCDTO(BaseModel):
    title_ru: DTOConstant.StandardVarcharField(description="Название роли на русском")
    title_kk: DTOConstant.StandardVarcharField(description="Название роли на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название роли на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание на английском"
    )
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение роли")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    can_register: DTOConstant.StandardBooleanFalseField(
        description="Доступна ли регистрация с этой ролью"
    )
    is_system: DTOConstant.StandardBooleanFalseField(description="Системная роль")
    is_administrative: DTOConstant.StandardBooleanFalseField(
        description="Административная роль"
    )

    class Config:
        from_attributes = True


class RoleRDTO(RoleDTO):
    title_ru: DTOConstant.StandardVarcharField(description="Название роли на русском")
    title_kk: DTOConstant.StandardVarcharField(description="Название роли на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название роли на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание на английском"
    )
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение роли")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    can_register: DTOConstant.StandardBooleanFalseField(
        description="Доступна ли регистрация с этой ролью"
    )
    is_system: DTOConstant.StandardBooleanFalseField(description="Системная роль")
    is_administrative: DTOConstant.StandardBooleanFalseField(
        description="Административная роль"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class RoleWithRelationsRDTO(RoleRDTO):
    permissions: list[PermissionRDTO] = []

    class Config:
        from_attributes = True
