from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.shared.dto_constants import DTOConstant


class SotaSportDTO(BaseModel):
    id: DTOConstant.StandardIntegerField()
    created_at: DTOConstant.StandardNullableDateTimeField()
    updated_at: DTOConstant.StandardNullableDateTimeField()
    name_ru: DTOConstant.StandardNullableVarcharField()
    name_en: DTOConstant.StandardNullableVarcharField()
    name_kk: DTOConstant.StandardNullableVarcharField()
    game_timer_type: DTOConstant.StandardNullableVarcharField()

    class Config:
        from_attributes = True


class SotaSportListDTO(BaseModel):
    count: DTOConstant.StandardIntegerField()
    next: DTOConstant.StandardNullableVarcharField()
    previous: DTOConstant.StandardNullableVarcharField()
    results: List[SotaSportDTO]

    class Config:
        from_attributes = True
