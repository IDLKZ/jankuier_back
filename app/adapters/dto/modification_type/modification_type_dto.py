from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class ModificationTypeDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ModificationTypeCDTO(BaseModel):
    title_ru: DTOConstant.StandardVarcharField(
        description="Название типа модификации на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название типа модификации на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название типа модификации на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение типа модификации"
    )

    class Config:
        from_attributes = True


class ModificationTypeRDTO(ModificationTypeDTO):
    title_ru: DTOConstant.StandardVarcharField(
        description="Название типа модификации на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название типа модификации на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название типа модификации на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение типа модификации"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True
