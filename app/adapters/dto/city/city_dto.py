from pydantic import BaseModel
from app.adapters.dto.country.country_dto import CountryRDTO
from app.shared.dto_constants import DTOConstant


class CityDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class CityCDTO(BaseModel):
    country_id: DTOConstant.StandardUnsignedIntegerField(description="ID страны")
    title_ru: DTOConstant.StandardVarcharField(description="Название города на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название города на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название города на английском")
    ticketon_city_id: DTOConstant.StandardNullableIntegerField(description="ID города в системе Ticketon")
    ticketon_tag: DTOConstant.StandardNullableVarcharField(description="Тег города в системе Ticketon")

    class Config:
        from_attributes = True


class CityRDTO(CityDTO):
    country_id: DTOConstant.StandardUnsignedIntegerField(description="ID страны")
    title_ru: DTOConstant.StandardVarcharField(description="Название города на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название города на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название города на английском")
    ticketon_city_id: DTOConstant.StandardNullableIntegerField(description="ID города в системе Ticketon")
    ticketon_tag: DTOConstant.StandardNullableVarcharField(description="Тег города в системе Ticketon")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class CityWithRelationsRDTO(CityRDTO):
    country: CountryRDTO | None = None

    class Config:
        from_attributes = True