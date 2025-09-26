from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import Optional

from app.adapters.dto.ticketon.ticketon_shows_dto import TicketonShowsDataDTO, TicketonGetShowsParameterDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.ticketon.ticketon_get_level_dto import TicketonGetLevelDTO
from app.adapters.dto.ticketon.ticketon_show_level_dto import TicketonShowLevelDTO
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.ticketon.get_ticketon_shows_case import GetTicketonShowsCase
from app.use_case.ticketon.get_ticketon_single_show_case import GetTicketonSingleShowCase
from app.use_case.ticketon.get_ticketon_level_case import GetTicketonLevelCase
from app.use_case.ticketon.get_ticketon_show_level_case import GetTicketonShowLevelCase


class TicketonApi:
    """
    API контроллер для работы с данными Ticketon.
    Предоставляет эндпоинты для получения информации о сеансах, событиях и местах.
    """
    
    def __init__(self) -> None:
        """
        Инициализация TicketonApi.
        Создаёт объект APIRouter и регистрирует маршруты для работы с Ticketon API.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """Регистрация маршрутов для Ticketon API"""
        
        self.router.get(
            "/shows",
            response_model=TicketonShowsDataDTO,
            summary="Получить данные о сеансах Ticketon",
            description="Получение информации о сеансах, событиях, местах и городах из Ticketon API с кешированием",
        )(self.get_shows)
        
        self.router.get(
            "/show/{show_id}",
            response_model=TicketonSingleShowResponseDTO,
            summary="Получить подробную информацию о сеансе",
            description="Получение детальной информации о конкретном сеансе включая схему зала и цены",
        )(self.get_single_show)

        self.router.get(
            "/level/{level_id}",
            response_model=TicketonGetLevelDTO,
            summary="Получить данные уровня зала",
            description="Получение подробных данных уровня зала по его идентификатору",
        )(self.get_level)

        self.router.get(
            "/show/{show_id}/level/{level_id}",
            response_model=TicketonShowLevelDTO,
            summary="Получить данные уровня зала для сеанса",
            description="Получение данных уровня зала для конкретного сеанса с информацией о местах и ценах",
        )(self.get_show_level)

    async def get_shows(
        self,
        place: Optional[int] = Query(
            default=None,
            description="ID площадки (place[]) - идентификатор места проведения",
            example=59
        ),
        event_type: Optional[str] = Query(
            default="sport",
            alias="type",
            description="Категория события (type[]) - тип мероприятия",
            example="sport"
        ),
        with_param: Optional[str] = Query(
            default="future",
            alias="with",
            description="Временной параметр (with[]) - показать будущие, прошедшие или все события",
            example="future"
        ),
        language: Optional[str] = Query(
            default="ru",
            alias="i18n",
            description="Язык локализации (i18n[]) - язык для получения данных",
            example="ru"
        ),
    ) -> TicketonShowsDataDTO:
        """
        Получение данных о сеансах из Ticketon API.
        
        Эндпоинт получает информацию о сеансах, событиях, местах проведения и городах 
        из внешнего API Ticketon с автоматическим кешированием в Redis.
        
        Args:
            place: ID площадки (место проведения)
            event_type: Тип события (sport, concert, theatre, cinema)
            with_param: Временной фильтр (future, past, all)
            language: Язык локализации (ru, kk, en)
            
        Returns:
            TicketonShowsDataDTO: Данные о сеансах с полной информацией
            
        Raises:
            HTTPException: При ошибках валидации или получения данных
        """
        try:
            # Создаём объект параметров
            parameter = TicketonGetShowsParameterDTO(
                place=place,
                type=event_type,
                withParam=with_param,
                i18n=language
            )
            
            # Выполняем use case
            return await GetTicketonShowsCase().execute(parameter)
            
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_single_show(
        self,
        show_id: int = Path(
            ...,
            description="ID сеанса для получения подробной информации",
            example=12345,
            gt=0
        ),
        i18n: Optional[str] = Query(
            default="ru",
            description="Язык локализации (i18n[]) - язык для получения данных",
            example="ru"
        ),
    ) -> TicketonSingleShowResponseDTO:
        """
        Получение подробной информации о конкретном сеансе из Ticketon API.
        
        Эндпоинт получает детальную информацию о сеансе включая:
        - Основную информацию о сеансе
        - Данные события
        - Информацию о месте проведения и городе
        - Схему зала с местами
        - Цены на билеты по категориям
        - Правила валидации мест
        
        Args:
            show_id: ID сеанса (должен быть положительным числом)
            
        Returns:
            TicketonSingleShowResponseDTO: Подробные данные о сеансе
            
        Raises:
            HTTPException: При ошибках валидации или получения данных
        """
        try:
            # Выполняем use case
            return await GetTicketonSingleShowCase().execute(show_id,i18n)
            
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc), "show_id": show_id},
                is_custom=True,
            ) from exc

    async def get_level(
        self,
        level_id: int = Path(
            ...,
            description="ID уровня зала для получения данных",
            example=594658,
            gt=0
        ),
    ) -> TicketonGetLevelDTO:
        """
        Получение данных уровня зала из Ticketon API.
        
        Эндпоинт получает подробную информацию об уровне зала включая:
        - Основную информацию о месте проведения
        - Данные зала
        - Характеристики уровня (размеры, SVG схема)
        - Список всех мест на уровне с координатами
        
        Args:
            level_id: ID уровня зала (должен быть положительным числом)
            
        Returns:
            TicketonGetLevelDTO: Данные уровня зала
            
        Raises:
            HTTPException: При ошибках валидации или получения данных
        """
        try:
            return await GetTicketonLevelCase().execute(level_id=level_id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc), "level_id": level_id},
                is_custom=True,
            ) from exc

    async def get_show_level(
        self,
        show_id: int = Path(
            ...,
            description="ID сеанса",
            example=12345,
            gt=0
        ),
        level_id: int = Path(
            ...,
            description="ID уровня зала",
            example=594658,
            gt=0
        ),
    ) -> TicketonShowLevelDTO:
        """
        Получение данных уровня зала для конкретного сеанса из Ticketon API.
        
        Эндпоинт получает информацию об уровне зала в контексте конкретного сеанса:
        - Схему зала с местами
        - Статус каждого места (свободно/занято/продано)
        - Типы билетов и цены
        - Объекты на схеме зала (ряды, входы и т.д.)
        - SVG данные для визуализации
        
        Args:
            show_id: ID сеанса (должен быть положительным числом)
            level_id: ID уровня зала (должен быть положительным числом)
            
        Returns:
            TicketonShowLevelDTO: Данные уровня зала для сеанса
            
        Raises:
            HTTPException: При ошибках валидации или получения данных
        """
        try:
            return await GetTicketonShowLevelCase().execute(
                show_id=show_id, level_id=level_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc), "show_id": show_id, "level_id": level_id},
                is_custom=True,
            ) from exc