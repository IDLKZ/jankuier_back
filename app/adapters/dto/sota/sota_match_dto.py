from typing import List
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class SotaTeamDTO(BaseModel):
    id: DTOConstant.StandardIntegerField("Уникальный идентификатор команды")
    name: DTOConstant.StandardNullableTextField("Название команды")
    score: DTOConstant.StandardNullableIntegerField("Счёт команды")


class SotaMatchDTO(BaseModel):
    id: DTOConstant.StandardTextField("Уникальный идентификатор матча")
    date: DTOConstant.StandardNullableTextField("Дата проведения матча")
    tournament_id: DTOConstant.StandardNullableIntegerField("Идентификатор турнира")
    home_team: SotaTeamDTO
    away_team: SotaTeamDTO
    tour: DTOConstant.StandardNullableIntegerField("Номер тура")
    has_stats: DTOConstant.StandardNullableBooleanField("Флаг: есть ли статистика")
    season_id: DTOConstant.StandardNullableIntegerField("Идентификатор сезона")
    season_name: DTOConstant.StandardNullableTextField("Название сезона")
    visitors: DTOConstant.StandardNullableIntegerField("Количество посетителей")
