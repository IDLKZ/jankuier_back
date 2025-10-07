from typing import List
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class SotaScoreTableTeamDTO(BaseModel):
    id: DTOConstant.StandardIntegerField("Уникальный идентификатор команды")
    name: DTOConstant.StandardNullableTextField("Название команды")
    logo: DTOConstant.StandardNullableTextField("URL логотипа команды")
    rg: DTOConstant.StandardNullableIntegerField("Разница голов")
    wins: DTOConstant.StandardNullableIntegerField("Количество побед")
    draws: DTOConstant.StandardNullableIntegerField("Количество ничьих")
    losses: DTOConstant.StandardNullableIntegerField("Количество поражений")
    points: DTOConstant.StandardNullableIntegerField("Количество очков")
    matches: DTOConstant.StandardNullableIntegerField("Количество сыгранных матчей")
    goals: DTOConstant.StandardNullableTextField("Голы (например '10-5')")


class SotaScoreTableDataDTO(BaseModel):
    latest_update_date_time: DTOConstant.StandardNullableTextField("Дата и время последнего обновления таблицы")
    table: List[SotaScoreTableTeamDTO]


class ScoreTableResponseDTO(BaseModel):
    result: DTOConstant.StandardNullableTextField("Результат ответа (например 'success')")
    data: SotaScoreTableDataDTO
