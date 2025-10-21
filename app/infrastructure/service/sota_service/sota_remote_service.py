import json
import traceback
from datetime import timedelta
from typing import Any, Optional, Type, List

import httpx
from loguru import logger
from pydantic import BaseModel

from app.adapters.dto.sota.sota_auth_token_dto import SotaTokenDTO
from app.adapters.dto.sota.sota_country_dto import SotaRemoteCountryDTO
from app.adapters.dto.sota.sota_match_dto import SotaMatchDTO
from app.adapters.dto.sota.sota_match_lineup_dto import SotaMatchLineupDTO
from app.adapters.dto.sota.sota_pagination_dto import SotaPaginationResponseDTO
from app.adapters.dto.sota.sota_parameters import CountryQueryDTO, TournamentQueryDTO, MatchQueryDTO
from app.adapters.dto.sota.sota_player_stat_dto import SotaPlayersStatsResponseDTO
from app.adapters.dto.sota.sota_score_table_team_dto import ScoreTableResponseDTO
from app.adapters.dto.sota.sota_team_stat_entity import SotaTeamsStatsResponseDTO
from app.adapters.dto.sota.sota_tournament_dto import SotaTournamentDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import redis_client
from app.infrastructure.service.redis_service import RedisService


class SotaRemoteService:

    def __init__(self):
        self.sota_access_token = "sota_access_token"
        self.ttl = app_config.sota_redis_save_minutes
        self.redis_service = RedisService()

    async def get_sota_token(self) -> str:
        token = self.redis_service.get_sota_token(self.sota_access_token)
        if token is None:
            params = {
                "email": app_config.sota_auth_email,
                "password": app_config.sota_auth_password
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(app_config.sota_auth_api, data=params)
                    data: SotaTokenDTO = SotaTokenDTO.parse_obj(response.json())
                    self.redis_service.set_sota_token(self.sota_access_token, data.access)
                    response.raise_for_status()
                    return data.access
                except Exception as e:
                    raise AppExceptionResponse.internal_error(
                        message=f"SOTA GET AUTH TOKEN ERROR: {str(e)}"  # noqa:RUF010,RUF100,
                    ) from e
        else:
            return token

    async def get_countries(self, dto: CountryQueryDTO, lang: str = "ru", use_redis: bool = True) -> \
    SotaPaginationResponseDTO[SotaRemoteCountryDTO]:
        token = await self.get_sota_token()
        url = app_config.sota_r_countries_api
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(dto.redis_key(lang), SotaPaginationResponseDTO[SotaRemoteCountryDTO])
                if data_cached:
                    return data_cached
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=dto.dict())
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = SotaPaginationResponseDTO[SotaRemoteCountryDTO].model_validate(json_data)
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(dto.redis_key(lang), result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET COUNTRIES [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_tournaments(self, dto: TournamentQueryDTO, lang: str = "ru", use_redis: bool = True) -> \
    SotaPaginationResponseDTO[SotaTournamentDTO]:
        token = await self.get_sota_token()
        url = app_config.sota_r_tournaments_api
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(dto.redis_key(lang), SotaPaginationResponseDTO[SotaTournamentDTO])
                if data_cached:
                    # Применяем сортировку к кешированным данным
                    priority_tournament_id = app_config.sota_priority_tournament_id
                    priority_tournaments = [t for t in data_cached.results if t.id == priority_tournament_id]
                    other_tournaments = [t for t in data_cached.results if t.id != priority_tournament_id]
                    data_cached.results = priority_tournaments + other_tournaments
                    return data_cached
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=dto.dict())
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = SotaPaginationResponseDTO[SotaTournamentDTO].model_validate(json_data)

                # 5. Сортировка: приоритетный турнир на первое место
                priority_tournament_id = app_config.sota_priority_tournament_id
                priority_tournaments = [t for t in result.results if t.id == priority_tournament_id]
                other_tournaments = [t for t in result.results if t.id != priority_tournament_id]
                result.results = priority_tournaments + other_tournaments

                # 6. Сохраняем в кеш
                if use_redis:
                    await self.set(dto.redis_key(lang), result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET TOURNAMENTS [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_matches(self, dto: MatchQueryDTO, lang: str = "ru", use_redis: bool = True) -> List[SotaMatchDTO]:
        token = await self.get_sota_token()
        url = app_config.sota_p_games_api
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                cached_data = await self.get(dto.redis_key(lang))
                if cached_data:
                    # Валидация за кешированных данных
                    if isinstance(cached_data, list):
                        return [SotaMatchDTO.model_validate(item) for item in cached_data]
                    return cached_data
            timeout = httpx.Timeout(None)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers, params=dto.dict())
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                if not isinstance(json_data, list):
                    raise ValueError(f"Expected list, got {type(json_data)}")
                result = [SotaMatchDTO.model_validate(item) for item in json_data]
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(dto.redis_key(lang), json_data, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET MATCHES [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_score_tables(self, season_id: int, lang: str = "ru", use_redis: bool = True) -> ScoreTableResponseDTO:
        token = await self.get_sota_token()
        url = f"{app_config.sota_p_base_season_api}{season_id}/score_table/"
        redis_key = f"{lang}_score_table_{season_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(redis_key, ScoreTableResponseDTO)
                if data_cached:
                    return data_cached
            timeout = httpx.Timeout(None)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = ScoreTableResponseDTO.model_validate(json_data)
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(redis_key, result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET SCORE TABLE [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_team_stat_by_game_id(self, game_id: str, lang: str = "ru",
                                       use_redis: bool = True) -> SotaTeamsStatsResponseDTO:
        token = await self.get_sota_token()
        url = f"{app_config.sota_p_games_api}{game_id}/teams/"
        redis_key = f"{lang}_game_team_stat_{game_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(redis_key, SotaTeamsStatsResponseDTO)
                if data_cached:
                    return data_cached
            timeout = httpx.Timeout(None)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = SotaTeamsStatsResponseDTO.model_validate(json_data)
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(redis_key, result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET TEAM STATS BY GAME ID [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_players_stat_by_game_id(self, game_id: str, lang: str = "ru",
                                          use_redis: bool = True) -> SotaPlayersStatsResponseDTO:
        token = await self.get_sota_token()
        url = f"{app_config.sota_p_games_api}{game_id}/players/"
        redis_key = f"{lang}_game_players_stat_{game_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(redis_key, SotaPlayersStatsResponseDTO)
                if data_cached:
                    return data_cached
            timeout = httpx.Timeout(None)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = SotaPlayersStatsResponseDTO.model_validate(json_data)
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(redis_key, result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET PLAYERS STATS BY GAME ID [{lang.upper()}] ERROR: {str(e)}"
            )

    async def get_pre_game_lineup_stat_by_game_id(self, game_id: str, lang: str = "ru",
                                                  use_redis: bool = True) -> SotaMatchLineupDTO:
        token = await self.get_sota_token()
        url = f"{app_config.sota_p_games_api}{game_id}/pre_game_lineup/"
        redis_key = f"{lang}_game_pre_game_lineup_stat_{game_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": lang
        }
        try:
            if use_redis:
                data_cached = await self.get(redis_key, SotaMatchLineupDTO)
                if data_cached:
                    return data_cached
            timeout = httpx.Timeout(None)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                # 4. Валидация в DTO
                result = SotaMatchLineupDTO.model_validate(json_data)
                # 5. Сохраняем в кеш
                if use_redis:
                    await self.set(redis_key, result, ttl=self.ttl)
                return result
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET PRE MATCH LINEUPS STATS BY GAME ID [{lang.upper()}] ERROR: {str(e)}"
            )

    async def preload_data(self):
        """
        Предзагрузка данных турниров, сезонов, матчей и турнирных таблиц в Redis кеш.
        Выполняется для всех языков: ru, en, kk.
        """
        try:
            logger.info("Starting SOTA data preload for all languages")
            for lang in ["ru", "en", "kk"]:
                logger.info(f"Preloading SOTA data for language: {lang}")
                try:
                    tournaments: SotaPaginationResponseDTO[SotaTournamentDTO] = await self.get_tournaments(
                        TournamentQueryDTO(
                            page=1,
                            page_size=50,
                            country=app_config.sota_kz_country_id
                        ),
                        lang
                    )

                    if tournaments is None or not tournaments.results:
                        logger.warning(f"No tournaments found for language: {lang}")
                        continue

                    logger.info(f"Found {len(tournaments.results)} tournaments for language: {lang}")

                    # Фильтруем турниры по критериям
                    excluded_season_ids = set(app_config.sota_excluded_season_ids)
                    filtered_tournaments = []

                    for tournament in tournaments.results:
                        # Проверка: только футбол
                        if tournament.sport != app_config.sota_kz_football_id:
                            logger.debug(f"Tournament {tournament.id} is not football, skipping")
                            continue

                        # Проверка: есть сезоны
                        if not tournament.seasons:
                            logger.debug(f"Tournament {tournament.id} has no seasons, skipping")
                            continue

                        # Проверка: есть изображение
                        if not tournament.image or not tournament.image.strip():
                            logger.debug(f"Tournament {tournament.id} has no image, skipping")
                            continue

                        # Проверка: нет исключенных сезонов
                        has_excluded_season = any(season.id in excluded_season_ids for season in tournament.seasons)
                        if has_excluded_season:
                            logger.debug(f"Tournament {tournament.id} has excluded seasons, skipping")
                            continue

                        filtered_tournaments.append(tournament)

                    logger.info(f"Filtered to {len(filtered_tournaments)} tournaments for language: {lang}")

                    for tournament in filtered_tournaments:
                        logger.info(
                            f"Processing tournament {tournament.id} ({tournament.name}) with {len(tournament.seasons)} seasons")

                        for season in tournament.seasons:
                            try:
                                logger.debug(f"Loading score table for season {season.id} ({season.name})")
                                await self.get_score_tables(season_id=season.id, lang=lang)
                            except Exception as exc:
                                logger.error(
                                    f"Error loading data for tournament {tournament.id}, season {season.id}: {str(exc)}")
                                traceback.print_exc()
                                continue
                            try:
                                logger.debug(f"Loading matches for tournament {tournament.id}, season {season.id}")
                                await self.get_matches(
                                    MatchQueryDTO(tournament_id=tournament.id, season_id=season.id),
                                    lang=lang)
                            except Exception as exc:
                                logger.error(
                                    f"Error loading data for tournament {tournament.id}, season {season.id}: {str(exc)}")
                                traceback.print_exc()
                                continue
                except Exception as exc:
                    logger.error(f"Error preloading data for language {lang}: {str(exc)}")
                    traceback.print_exc()
                    continue

            logger.info("SOTA data preload completed")

        except Exception as exc:
            logger.error(f"Critical error in preload_data: {str(exc)}")
            traceback.print_exc()

    async def get(self, cache_key: str, dto_class: Optional[Type[Any]] = None) -> Optional[Any]:
        """
        Получает данные из Redis кэша.

        Args:
            cache_key: Ключ кэша
            dto_class: Класс DTO (BaseModel) для десериализации

        Returns:
            DTO, dict или None
        """
        try:
            cached_data = redis_client.get(cache_key)
            if not cached_data:
                return None

            # Если передан DTO класс → валидируем через него
            if dto_class:
                return dto_class.model_validate_json(cached_data)

            # Если нет DTO → просто возвращаем dict
            return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Redis cache get error for key {cache_key}: {e}")
            return None

    async def set(self, cache_key: str, data: Any, ttl: Optional[timedelta | int] = None) -> None:
        """
        Сохраняет данные в Redis кэш.

        Args:
            cache_key: Ключ кэша
            data: Данные для сохранения (BaseModel, dict, list, str)
            ttl: Время жизни (timedelta или int секунд). По умолчанию self.ttl минут
        """
        try:
            if isinstance(ttl, timedelta):
                ttl_seconds = int(ttl.total_seconds())
            elif ttl is not None:
                ttl_seconds = ttl
            else:
                # self.ttl в минутах, конвертируем в секунды
                ttl_seconds = self.ttl * 60

            if isinstance(data, BaseModel):
                payload = data.model_dump_json()
            elif isinstance(data, (dict, list)):
                payload = json.dumps(data, ensure_ascii=False)
            elif isinstance(data, str):
                payload = data
            else:
                payload = json.dumps(data, default=str, ensure_ascii=False)

            redis_client.setex(cache_key, ttl_seconds, payload)
        except Exception as e:
            logger.warning(f"Redis cache set error for key {cache_key}: {e}")
