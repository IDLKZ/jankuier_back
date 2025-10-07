from typing import Optional, List

from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class SotaCountryDTO(BaseModel):
    id: DTOConstant.StandardID()
    name_ru: DTOConstant.StandardTextField()
    name_kk: DTOConstant.StandardNullableTextField()
    name_en: DTOConstant.StandardNullableTextField()
    flag_image: DTOConstant.StandardNullableTextField()
    code: DTOConstant.StandardNullableVarcharField()

    class Config:
        from_attributes = True

class SotaCountryListDTO(BaseModel):
    count: DTOConstant.StandardIntegerField()
    next: DTOConstant.StandardNullableTextField()
    previous: DTOConstant.StandardNullableTextField()
    results: List[SotaCountryDTO]

    class Config:
        from_attributes = True


class SotaRemoteCountryDTO(BaseModel):
    id: DTOConstant.StandardID("Уникальный идентификатор страны")
    name: DTOConstant.StandardNullableTextField("Название страны")
    flag_image: DTOConstant.StandardNullableTextField("URL флага страны")
    code: DTOConstant.StandardVarcharField("Код страны (ISO)")

    class Config:
        from_attributes = True
