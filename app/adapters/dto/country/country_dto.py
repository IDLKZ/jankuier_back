from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class CountryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class CountryCDTO(BaseModel):
    title_ru: DTOConstant.StandardVarcharField(description="Название страны на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название страны на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название страны на английском")
    sota_code: DTOConstant.StandardNullableVarcharField(description="Код страны SOTA")
    sota_flag_image: DTOConstant.StandardNullableTextField(description="URL флага страны")

    class Config:
        from_attributes = True


class CountryRDTO(CountryDTO):
    title_ru: DTOConstant.StandardVarcharField(description="Название страны на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название страны на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название страны на английском")
    sota_code: DTOConstant.StandardNullableVarcharField(description="Код страны SOTA")
    sota_flag_image: DTOConstant.StandardNullableTextField(description="URL флага страны")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True