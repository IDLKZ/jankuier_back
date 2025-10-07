from typing import List, Optional
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class SotaPlayerStatsDTO(BaseModel):
    shot: DTOConstant.StandardNullableIntegerField("Удары всего")
    shots_on_goal: DTOConstant.StandardNullableIntegerField("Удары в створ")
    shots_off_goal: DTOConstant.StandardNullableIntegerField("Удары мимо ворот")
    foul: DTOConstant.StandardNullableIntegerField("Фолы")
    yellow_cards: DTOConstant.StandardNullableIntegerField("Жёлтые карточки")
    red_cards: DTOConstant.StandardNullableIntegerField("Красные карточки")
    pass_: DTOConstant.StandardNullableIntegerField("Передачи") = Field(..., alias="pass")
    offside: DTOConstant.StandardNullableIntegerField("Офсайды")
    corner: DTOConstant.StandardNullableIntegerField("Угловые")
    duel: DTOConstant.StandardNullableIntegerField("Единоборства")
    tackle: DTOConstant.StandardNullableIntegerField("Отборы")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class SotaPlayerDTO(BaseModel):
    id: DTOConstant.StandardNullableTextField("Уникальный идентификатор игрока")
    team: DTOConstant.StandardNullableTextField("Название команды игрока")
    number: DTOConstant.StandardNullableIntegerField("Игровой номер игрока")
    first_name: DTOConstant.StandardNullableTextField("Имя игрока")
    last_name: DTOConstant.StandardNullableTextField("Фамилия игрока")
    stats: SotaPlayerStatsDTO


class SotaPlayersStatsDataDTO(BaseModel):
    latest_update_date_time: Optional[
        DTOConstant.StandardNullableTextField("Дата и время последнего обновления статистики игроков")
    ]
    players: List[SotaPlayerDTO]


class SotaPlayersStatsResponseDTO(BaseModel):
    result: DTOConstant.StandardNullableTextField("Результат ответа (например 'success')")
    data: SotaPlayersStatsDataDTO
