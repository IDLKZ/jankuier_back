from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class PermissionDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class PermissionCDTO(BaseModel):
    title_ru: DTOConstant.StandardVarcharField(description="Название разрешения (RU)")
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название разрешения (KZ)"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название разрешения (EN)"
    )
    value: DTOConstant.StandardNullableUniqueValueField(
        description="Уникальное значение разрешения"
    )

    class Config:
        from_attributes = True


class PermissionRDTO(PermissionDTO):
    title_ru: DTOConstant.StandardVarcharField(description="Название разрешения (RU)")
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название разрешения (KZ)"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название разрешения (EN)"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение разрешения"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True
