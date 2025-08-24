from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class TicketonCityDTO(BaseModel):
    city_id: DTOConstant.StandardID("ID города из Ticketon")
    tag: DTOConstant.StandardNullableVarcharField("Slug/тег города (может быть пустым)")
    name: DTOConstant.StandardVarcharField("Название (ru)")
    name_en: DTOConstant.StandardNullableVarcharField("Название (en)")
    name_kz: DTOConstant.StandardNullableVarcharField("Название (kk)")
    sort: DTOConstant.StandardUnsignedIntegerField("Порядок сортировки")
    is_enabled: DTOConstant.StandardBooleanTrueField("Признак активности")
    timezone: DTOConstant.StandardVarcharField("Часовой пояс IANA (например, Asia/Almaty)")
    timeshift: DTOConstant.StandardVarcharField("Сдвиг времени (например, GMT+6)")
    country_id: DTOConstant.StandardUnsignedIntegerField("ID страны")

    class Config:
        from_attributes = True