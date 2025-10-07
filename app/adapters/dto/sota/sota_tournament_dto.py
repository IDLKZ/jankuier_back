from typing import List, Optional
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class SotaTournamentSeasonDTO(BaseModel):
    id: DTOConstant.StandardIntegerField("Уникальный идентификатор сезона")
    name: DTOConstant.StandardNullableTextField("Название сезона")
    start_date: DTOConstant.StandardNullableTextField("Дата начала сезона")
    end_date: DTOConstant.StandardNullableTextField("Дата окончания сезона")
    teams: DTOConstant.StandardNullableIntegerArrayField("Список идентификаторов команд")


class SotaTournamentDTO(BaseModel):
    id: DTOConstant.StandardIntegerField("Уникальный идентификатор турнира")
    name: DTOConstant.StandardNullableTextField("Название турнира")
    created_at: DTOConstant.StandardDateTimeField("Дата создания записи")
    updated_at: DTOConstant.StandardDateTimeField("Дата обновления записи")
    is_international: DTOConstant.StandardNullableBooleanField("Флаг: международный турнир")
    image: DTOConstant.StandardNullableTextField("URL изображения турнира")
    show_in_stats: DTOConstant.StandardNullableBooleanField("Флаг: отображать в статистике")
    last_full_calculated_at: DTOConstant.StandardNullableDateTimeField("Дата последнего пересчёта статистики")
    is_male: DTOConstant.StandardNullableBooleanField("Флаг: мужской турнир")
    sport: DTOConstant.StandardNullableIntegerField("Идентификатор спорта")
    seasons: List[SotaTournamentSeasonDTO]
