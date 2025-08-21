from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class SportDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class SportCDTO(BaseModel):
    title_ru: DTOConstant.StandardVarcharField(
        description="Название вида спорта на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название вида спорта на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название вида спорта на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение вида спорта"
    )

    class Config:
        from_attributes = True


class SportRDTO(SportDTO):
    title_ru: DTOConstant.StandardVarcharField(
        description="Название вида спорта на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название вида спорта на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название вида спорта на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение вида спорта"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True
