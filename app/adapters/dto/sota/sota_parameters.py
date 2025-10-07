from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from app.infrastructure.app_config import app_config


class CountryQueryDTO(BaseModel):
    page: int = Query(app_config.sota_kz_country_id, gt=0, description="Номер страницы (по умолчанию 112)")
    page_size: int = Query(1, gt=0, le=250, description="Количество элементов на странице (по умолчанию 1)")

    def redis_key(self,lang: str) -> str:
        """
        Генерация ключа для Redis-кеша
        """
        return f"sota_countries_{lang}_{self.page}_{self.page_size}"


class TournamentQueryDTO(BaseModel):
    page: int = Query(1, gt=0, description="Номер страницы (по умолчанию 1)")
    page_size: int = Query(50, gt=0, le=250, description="Количество элементов на странице (по умолчанию 50)")
    id: Optional[int] = Query(None, gt=0, description="Опциональный идентификатор турнира")
    country: int = Query(app_config.sota_kz_country_id, gt=0, description="ID страны (по умолчанию Казахстан)")
    is_male: Optional[bool] = Query(None, description="Флаг: мужской турнир")
    search: Optional[str] = Query(None, min_length=2, max_length=255, description="Поисковый запрос")
    team: Optional[int] = Query(None, gt=0, description="Идентификатор команды")

    def redis_key(self,lang: str) -> str:
        """
        Генерация уникального ключа для Redis-кеша
        """
        key_parts = [
            f"page={self.page}",
            f"page_size={self.page_size}",
            f"country={self.country}",
        ]
        if self.id is not None:
            key_parts.append(f"id={self.id}")
        if self.is_male is not None:
            key_parts.append(f"is_male={int(self.is_male)}")  # True -> 1, False -> 0
        if self.search is not None:
            key_parts.append(f"search={self.search}")
        if self.team is not None:
            key_parts.append(f"team={self.team}")

        return f"sota_tournaments_{lang}_" + "_".join(key_parts)


class MatchQueryDTO(BaseModel):
    season_id: int = Query(1, gt=0, description="ID сезона (по умолчанию SotaApiConstant.SeasonId)")
    tournament_id: int = Query(1, gt=0, description="ID турнира (по умолчанию SotaApiConstant.TournamentId)")
    away_team_id: Optional[int] = Query(None, gt=0, description="ID гостевой команды")
    home_team_id: Optional[int] = Query(None, gt=0, description="ID домашней команды")
    date_from: Optional[date] = Query(None, description="Дата начала периода (гггг-мм-дд)")
    date_to: Optional[date] = Query(None, description="Дата конца периода (гггг-мм-дд)")
    player_id: Optional[int] = Query(None, gt=0, description="ID игрока")
    team: Optional[int] = Query(None, gt=0, description="ID команды")

    def redis_key(self,lang: str) -> str:
        """
        Генерация уникального ключа для Redis-кеша матчей
        """
        key_parts = [
            f"season_id={self.season_id}",
            f"tournament_id={self.tournament_id}",
        ]
        if self.away_team_id is not None:
            key_parts.append(f"away_team_id={self.away_team_id}")
        if self.home_team_id is not None:
            key_parts.append(f"home_team_id={self.home_team_id}")
        if self.date_from is not None:
            key_parts.append(f"date_from={self.date_from.isoformat()}")
        if self.date_to is not None:
            key_parts.append(f"date_to={self.date_to.isoformat()}")
        if self.player_id is not None:
            key_parts.append(f"player_id={self.player_id}")
        if self.team is not None:
            key_parts.append(f"team={self.team}")

        return f"sota_matches__{lang}_" + "_".join(key_parts)