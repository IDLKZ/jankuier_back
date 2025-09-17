import json
from datetime import timedelta, datetime
from typing import Union, List, Optional, Dict, Any

import httpx
from pydantic import TypeAdapter

from app.adapters.dto.ticketon.ticketon_booking_dto import (
    TicketonBookingErrorResponseDTO,
    TicketonBookingShowBookingDTO,
    TicketonBookingRequestDTO
)
from app.adapters.dto.ticketon.ticketon_city_dto import TicketonCityDTO
from app.adapters.dto.ticketon.ticketon_confirm_sale_dto import (
    TicketonConfirmSaleRequestDTO,
    TicketonConfirmSaleResponseDTO
)
from app.adapters.dto.ticketon.ticketon_get_level_dto import TicketonGetLevelDTO
from app.adapters.dto.ticketon.ticketon_order_check_response_dto import TicketonOrderCheckResponseDTO
from app.adapters.dto.ticketon.ticketon_refund_request_dto import TicketonSaleRefundResponseDTO
from app.adapters.dto.ticketon.ticketon_show_level_dto import TicketonShowLevelDTO
from app.adapters.dto.ticketon.ticketon_shows_dto import (
    TicketonShowsDataDTO,
    TicketonGetShowsParameterDTO,
    TicketonShowsRedisStore
)
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.ticketon.ticketon_ticket_check_response_dto import TicketonTicketCheckResponseDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import redis_client


class TicketonServiceAPI:
    """
    Сервис для работы с API Ticketon.

    Предоставляет методы для:
    - Получения информации о городах, событиях и залах
    - Бронирования и продажи билетов
    - Проверки заказов и билетов
    - Отмены и возврата билетов

    Использует Redis для кэширования запросов с настраиваемым TTL.
    """

    def __init__(self) -> None:
        """Инициализация сервиса Ticketon API."""
        self._client_timeout = 30.0
        self._redis_ttl = timedelta(minutes=app_config.ticketon_update_redis_in_minutes)

    async def _make_request(
        self,
        url: str,
        params: Dict[str, Any],
        operation_name: str
    ) -> Dict[str, Any]:
        """
        Выполняет HTTP-запрос к API Ticketon.

        Args:
            url: URL для запроса
            params: Параметры запроса
            operation_name: Название операции для логирования ошибок

        Returns:
            Dict[str, Any]: JSON-ответ от API

        Raises:
            AppExceptionResponse: При ошибке запроса или парсинга ответа
        """
        try:
            # Добавляем токен авторизации
            params["token"] = app_config.ticketon_api_key

            async with httpx.AsyncClient(timeout=self._client_timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon {operation_name} HTTP error: {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon {operation_name} request error: {str(e)}"
            ) from e
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon {operation_name} error: {str(e)}"
            ) from e

    def _get_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Генерирует ключ для Redis кэша.

        Args:
            prefix: Префикс ключа
            **kwargs: Параметры для ключа

        Returns:
            str: Ключ для кэширования
        """
        key_parts = [prefix] + [f"{k}_{v}" for k, v in sorted(kwargs.items())]
        return "_".join(str(part) for part in key_parts)

    async def _get_from_cache(self, cache_key: str, dto_class) -> Optional[Any]:
        """
        Получает данные из Redis кэша.

        Args:
            cache_key: Ключ кэша
            dto_class: Класс DTO для десериализации

        Returns:
            Optional[Any]: Объект DTO или None если данных нет
        """
        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return dto_class.model_validate_json(cached_data)
        except Exception as e:
            print(f"[WARN] Redis cache error for key {cache_key}: {e}")
        return None

    def _set_cache(self, cache_key: str, data: Any, ttl: Optional[timedelta] = None) -> None:
        """
        Сохраняет данные в Redis кэш.

        Args:
            cache_key: Ключ кэша
            data: Данные для сохранения
            ttl: Время жизни кэша (по умолчанию из конфигурации)
        """
        try:
            ttl = ttl or self._redis_ttl
            if hasattr(data, 'model_dump_json'):
                redis_client.setex(cache_key, ttl, data.model_dump_json())
            else:
                redis_client.setex(cache_key, ttl, json.dumps(data, ensure_ascii=False))
        except Exception as e:
            print(f"[WARN] Redis cache set error for key {cache_key}: {e}")

    # === МЕТОДЫ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ===

    async def get_ticketon_cities(self) -> List[TicketonCityDTO]:
        """
        Получает список городов из API Ticketon.

        Returns:
            List[TicketonCityDTO]: Список городов

        Raises:
            AppExceptionResponse: При ошибке получения данных
        """
        json_data = await self._make_request(
            url=app_config.ticketon_get_cities,
            params={},
            operation_name="get cities"
        )
        return [TicketonCityDTO.model_validate(item) for item in json_data]

    async def get_ticketon_shows(
        self,
        parameter: TicketonGetShowsParameterDTO
    ) -> TicketonShowsDataDTO:
        """
        Получает список событий с кэшированием в Redis только при наличии place.

        Args:
            parameter: Параметры поиска событий

        Returns:
            TicketonShowsDataDTO: Данные о событиях

        Raises:
            AppExceptionResponse: При ошибке получения данных
        """
        # Используем Redis только если указан place
        cached_data = None
        cache_key = None

        if parameter.place is not None:
            cache_key = self._get_cache_key(
                "shows",
                type=parameter.type,
                place=parameter.place,
                withParam=parameter.withParam,
                i18n=parameter.i18n
            )
            cached_data = await self._get_from_cache(cache_key, TicketonShowsRedisStore)
            if cached_data and cached_data.data.shows:
                if cached_data.last_updated + self._redis_ttl > datetime.now():
                    return cached_data.data

        # Запрос к API
        params = {
            f"type[]": parameter.type,
            f"with[]": parameter.withParam,
            "i18n": parameter.i18n
        }

        # Добавляем place только если он указан
        if parameter.place is not None:
            params[f"place[]"] = parameter.place

        json_data = await self._make_request(
            url=app_config.ticketon_get_shows,
            params=params,
            operation_name="get shows"
        )

        data = TicketonShowsDataDTO.from_json(json_data)

        # Сохраняем в кэш только если указан place
        if parameter.place is not None and cache_key is not None:
            redis_store = TicketonShowsRedisStore(
                query=parameter,
                data=data,
                last_updated=datetime.now()
            )
            self._set_cache(cache_key, redis_store)

        return data

    async def get_ticketon_single_show(
        self,
        show_id: int,
        use_cache: bool = True
    ) -> TicketonSingleShowResponseDTO:
        """
        Получает детальную информацию о событии.

        Args:
            show_id: ID события
            use_cache: Использовать кэширование

        Returns:
            TicketonSingleShowResponseDTO: Детальная информация о событии

        Raises:
            AppExceptionResponse: При ошибке получения данных
        """
        cache_key = f"single_show_{show_id}"

        # Проверяем кэш
        if use_cache:
            cached_data = await self._get_from_cache(cache_key, TicketonSingleShowResponseDTO)
            if cached_data:
                return cached_data

        # Запрос к API
        params = {"id": show_id}
        json_data = await self._make_request(
            url=app_config.ticketon_get_show,
            params=params,
            operation_name="get single show"
        )

        data = TicketonSingleShowResponseDTO.model_validate(json_data)

        # Сохраняем в кэш
        if use_cache:
            self._set_cache(cache_key, data)

        return data

    async def get_ticketon_show_level(
        self,
        show_id: int,
        level_id: int
    ) -> TicketonShowLevelDTO:
        """
        Получает информацию об уровне/секторе события.

        Args:
            show_id: ID события
            level_id: ID уровня/сектора

        Returns:
            TicketonShowLevelDTO: Информация об уровне события

        Raises:
            AppExceptionResponse: При ошибке получения данных
        """
        params = {
            "id": show_id,
            "level": level_id
        }

        json_data = await self._make_request(
            url=app_config.ticketon_show_level,
            params=params,
            operation_name="get show level"
        )

        return TicketonShowLevelDTO.from_json(json_data)

    async def get_ticketon_level(self, level_id: int) -> TicketonGetLevelDTO:
        """
        Получает информацию об уровне/секторе по ID.

        Args:
            level_id: ID уровня/сектора

        Returns:
            TicketonGetLevelDTO: Информация об уровне

        Raises:
            AppExceptionResponse: При ошибке получения данных
        """
        params = {"id": level_id}

        json_data = await self._make_request(
            url=app_config.ticketon_get_level,
            params=params,
            operation_name="get level"
        )

        return TicketonGetLevelDTO.from_json(json_data)

    # === МЕТОДЫ ДЛЯ ПРОВЕРКИ ===

    async def check_order(
        self,
        sale: str,
        date_format: str = "Y-m-d%20H:i"
    ) -> TicketonOrderCheckResponseDTO:
        """
        Проверяет статус заказа в системе Ticketon.

        Args:
            sale: ID заказа для проверки
            date_format: Формат даты в ответе

        Returns:
            TicketonOrderCheckResponseDTO: Информация о заказе

        Raises:
            AppExceptionResponse: При ошибке проверки заказа
        """
        params = {
            "sale": sale,
            "date_format": date_format
        }

        json_data = await self._make_request(
            url=app_config.ticketon_order_check,
            params=params,
            operation_name="check order"
        )

        return TicketonOrderCheckResponseDTO.from_json(json_data)

    async def check_ticket(self, ticket_id: str) -> TicketonTicketCheckResponseDTO:
        """
        Проверяет статус билета в системе Ticketon.

        Args:
            ticket_id: ID билета для проверки

        Returns:
            TicketonTicketCheckResponseDTO: Информация о билете

        Raises:
            AppExceptionResponse: При ошибке проверки билета
        """
        params = {"ticket": ticket_id}

        json_data = await self._make_request(
            url=app_config.ticketon_ticket_check,
            params=params,
            operation_name="check ticket"
        )

        return TicketonTicketCheckResponseDTO.from_json(json_data)

    # === МЕТОДЫ ДЛЯ ПРОДАЖ ===

    async def sale_ticketon(
        self,
        dto: TicketonBookingRequestDTO
    ) -> Union[TicketonBookingShowBookingDTO, TicketonBookingErrorResponseDTO]:
        """
        Создает бронирование билетов в системе Ticketon.

        Args:
            dto: Данные для бронирования

        Returns:
            Union[TicketonBookingShowBookingDTO, TicketonBookingErrorResponseDTO]:
                Результат бронирования или ошибка

        Raises:
            AppExceptionResponse: При ошибке создания бронирования
        """
        params = {
            "lang": dto.lang,
            "show": dto.show,
        }

        # Добавляем места как массив
        for i, seat in enumerate(dto.seats):
            params[f"seats[{i}]"] = seat

        json_data = await self._make_request(
            url=app_config.ticketon_create_sale,
            params=params,
            operation_name="create sale"
        )

        adapter = TypeAdapter(
            Union[TicketonBookingShowBookingDTO, TicketonBookingErrorResponseDTO]
        )
        return adapter.validate_python(json_data)

    async def sale_confirm(
        self,
        dto: TicketonConfirmSaleRequestDTO
    ) -> TicketonConfirmSaleResponseDTO:
        """
        Подтверждает продажу билетов в системе Ticketon.

        Args:
            dto: Данные для подтверждения продажи

        Returns:
            TicketonConfirmSaleResponseDTO: Результат подтверждения

        Raises:
            AppExceptionResponse: При ошибке подтверждения продажи
        """
        params = {
            "sale": dto.sale,
            "email": dto.email,
            "phone": dto.phone
        }

        json_data = await self._make_request(
            url=app_config.ticketon_sale_confirm,
            params=params,
            operation_name="confirm sale"
        )

        return TicketonConfirmSaleResponseDTO.model_validate(json_data)

    async def sale_cancel(self, sale_id: str) -> Dict[str, Any]:
        """
        Отменяет продажу билетов в системе Ticketon.

        Args:
            sale_id: ID продажи для отмены

        Returns:
            Dict[str, Any]: Результат операции отмены

        Raises:
            AppExceptionResponse: При ошибке отмены продажи
        """
        params = {"sale": sale_id}

        return await self._make_request(
            url=app_config.ticketon_sale_cancel,
            params=params,
            operation_name="cancel sale"
        )

    async def sale_refund(self, sale_id: str) -> TicketonSaleRefundResponseDTO:
        """
        Создает запрос на возврат билетов в системе Ticketon.

        Args:
            sale_id: ID продажи для возврата

        Returns:
            TicketonSaleRefundResponseDTO: Результат операции возврата

        Raises:
            AppExceptionResponse: При ошибке возврата билетов
        """
        params = {"sale": sale_id}

        json_data = await self._make_request(
            url=app_config.ticketon_sale_refund,
            params=params,
            operation_name="refund sale"
        )

        return TicketonSaleRefundResponseDTO(
            status=json_data.get('status', 0),
            error=json_data.get('error'),
            code=json_data.get('code')
        )

    # === ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ===

    def get_redis_for_shows_key(self, parameter: TicketonGetShowsParameterDTO) -> str:
        """
        Генерирует ключ Redis для кэширования событий.

        Args:
            parameter: Параметры поиска событий

        Returns:
            str: Ключ для Redis

        Note:
            Deprecated: Используйте _get_cache_key() вместо этого метода
        """
        return self._get_cache_key(
            "shows",
            type=parameter.type,
            place=parameter.place,
            withParam=parameter.withParam,
            i18n=parameter.i18n
        )