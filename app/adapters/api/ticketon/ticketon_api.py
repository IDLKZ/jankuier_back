from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import Optional

from app.adapters.dto.ticketon.ticketon_shows_dto import TicketonShowsDataDTO, TicketonGetShowsParameterDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.ticketon.get_ticketon_shows_case import GetTicketonShowsCase
from app.use_case.ticketon.get_ticketon_single_show_case import GetTicketonSingleShowCase


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

    async def get_shows(
        self,
        place: Optional[int] = Query(
            default=59,
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
        i18n: Optional[str] = Query(
            default="ru",
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
            i18n: Язык локализации (ru, kk, en)
            
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
                i18n=i18n
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
            return await GetTicketonSingleShowCase().execute(show_id)
            
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc), "show_id": show_id},
                is_custom=True,
            ) from exc