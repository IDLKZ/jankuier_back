import traceback
from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, Header

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
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.sota_service.sota_remote_service import SotaRemoteService
from app.shared.route_constants import RoutePathConstants


class SotaApi:
    def __init__(self) -> None:
        """
        Инициализация SportApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API видов спорта.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            "/registers/countries",
            response_model=SotaPaginationResponseDTO[SotaRemoteCountryDTO],
            summary="Список видов стран с пагинацией",
            description="Получение списка стран постраничной фильтрацией",
        )(self.get_sota_countries)

        self.router.get(
            "/registers/tournaments",
            response_model=SotaPaginationResponseDTO[SotaTournamentDTO],
            summary="Список видов турниров с пагинацией",
            description="Получение списка турниров постраничной фильтрацией",
        )(self.get_sota_tournaments)

        self.router.get(
            "/public/v1/games",
            response_model=List[SotaMatchDTO],
            summary="Список матчей",
            description="Получение списка матчей фильтрацией",
        )(self.get_matches)

        self.router.get(
            "/public/v1/seasons/{seasonId}/score_table",
            response_model=ScoreTableResponseDTO,
            summary="Турнирная таблица",
            description="Получение списка турнирной таблицы",
        )(self.get_score_table)

        self.router.get(
            "/public/v1/games/{gameId}/teams",
            response_model=SotaTeamsStatsResponseDTO,
            summary="Статистика команд по матчу",
            description="Получение статистики команд для конкретного матча",
        )(self.get_team_stat_by_game_id)

        self.router.get(
            "/public/v1/games/{gameId}/players",
            response_model=SotaPlayersStatsResponseDTO,
            summary="Статистика игроков по матчу",
            description="Получение статистики игроков для конкретного матча",
        )(self.get_players_stat_by_game_id)

        self.router.get(
            "/public/v1/games/{gameId}/pre_game_lineup",
            response_model=SotaMatchLineupDTO,
            summary="Предматчевый состав",
            description="Получение предматчевого состава команд",
        )(self.get_pre_game_lineup_stat_by_game_id)

        self.router.post(
            "/preload-data",
            response_model=dict,
            summary="Предзагрузка данных SOTA",
            description="Предзагрузка турниров, сезонов, матчей и турнирных таблиц в Redis кеш для всех языков",
        )(self.preload_data)

    async def get_sota_countries(
        self,
        dto: CountryQueryDTO = Depends(),
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> SotaPaginationResponseDTO[SotaRemoteCountryDTO]:
        try:
            return await SotaRemoteService().get_countries(dto=dto, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc


    async def get_sota_tournaments(
        self,
        dto: TournamentQueryDTO = Depends(),
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> SotaPaginationResponseDTO[SotaTournamentDTO]:
        try:
            return await SotaRemoteService().get_tournaments(dto=dto, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc


    async def get_matches(
        self,
        dto: MatchQueryDTO = Depends(),
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> List[SotaMatchDTO]:
        try:
            return await SotaRemoteService().get_matches(dto=dto, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_score_table(
        self,
        seasonId: RoutePathConstants.IDPath,
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> ScoreTableResponseDTO:
        try:
            return await SotaRemoteService().get_score_tables(season_id=seasonId, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_team_stat_by_game_id(
        self,
        gameId: str,
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> SotaTeamsStatsResponseDTO:
        try:
            return await SotaRemoteService().get_team_stat_by_game_id(game_id=gameId, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_players_stat_by_game_id(
        self,
        gameId: str,
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> SotaPlayersStatsResponseDTO:
        try:
            return await SotaRemoteService().get_players_stat_by_game_id(game_id=gameId, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_pre_game_lineup_stat_by_game_id(
        self,
        gameId: str,
        accept_language: str = Header(default="ru", alias="Accept-Language")
    ) -> SotaMatchLineupDTO:
        try:
            return await SotaRemoteService().get_pre_game_lineup_stat_by_game_id(game_id=gameId, lang=accept_language, use_redis=True)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def preload_data(self) -> dict:
        try:
            await SotaRemoteService().preload_data()
            return {
                "status": "success",
                "message": "SOTA data preload started successfully"
            }
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc