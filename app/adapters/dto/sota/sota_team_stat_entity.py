from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class SotaTeamStatsDTO(BaseModel):
    possession: Optional[Any] = None
    shot: Optional[int] = Field(None, description="Удары всего")
    shots_on_goal: Optional[int] = Field(None, description="Удары в створ")
    shots_off_goal: Optional[int] = Field(None, description="Удары мимо ворот")
    foul: Optional[int] = Field(None, description="Фолы")
    yellow_cards: Optional[int] = Field(None, description="Жёлтые карточки")
    red_cards: Optional[int] = Field(None, description="Красные карточки")
    pass_: Optional[int] = Field(None, description="Передачи", alias="pass")
    offside: Optional[int] = Field(None, description="Офсайды")
    corner: Optional[int] = Field(None, description="Угловые")

    class Config:
        populate_by_name = True


class SotaTeamWithStatsDTO(BaseModel):
    id: DTOConstant.StandardNullableIntegerField("Уникальный идентификатор команды")
    name: DTOConstant.StandardNullableTextField("Название команды")
    stats: Dict[str, Any] = Field(default_factory=dict, description="Статистика команды")


class SotaTeamsStatsDataDTO(BaseModel):
    latest_update_date_time: Optional[
        DTOConstant.StandardNullableTextField("Дата и время последнего обновления статистики")
    ]
    teams: List[SotaTeamWithStatsDTO]


class SotaTeamsStatsResponseDTO(BaseModel):
    result: DTOConstant.StandardNullableTextField("Результат ответа (например 'success')")
    data: SotaTeamsStatsDataDTO
