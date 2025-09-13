import json
from datetime import timedelta, datetime
from typing import Union

import httpx
from pydantic import TypeAdapter

from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingErrorResponseDTO, \
    TicketonBookingShowBookingDTO, TicketonBookingRequestDTO
from app.adapters.dto.ticketon.ticketon_city_dto import TicketonCityDTO
from app.adapters.dto.ticketon.ticketon_confirm_sale_dto import TicketonConfirmSaleRequestDTO, \
    TicketonConfirmSaleResponseDTO
from app.adapters.dto.ticketon.ticketon_get_level_dto import TicketonGetLevelDTO
from app.adapters.dto.ticketon.ticketon_refund_request_dto import TicketonSaleRefundResponseDTO
from app.adapters.dto.ticketon.ticketon_show_level_dto import TicketonShowLevelDTO
from app.adapters.dto.ticketon.ticketon_shows_dto import TicketonShowsDataDTO, TicketonGetShowsParameterDTO, \
    TicketonShowsRedisStore
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.redis_client import redis_client


class TicketonServiceAPI:
    def __init__(self):
        pass


    async def get_ticketon_cities(self)->list[TicketonCityDTO]:
        url = app_config.ticketon_get_cities
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                return [TicketonCityDTO.parse_obj(item) for item in json_data]
        except Exception as e:
                raise AppExceptionResponse.internal_error(
                    message=f"Ticketon GET cities ERROR: {str(e)}"
                ) from e


    async def get_ticketon_shows(self,parameter:TicketonGetShowsParameterDTO)->TicketonShowsDataDTO:
        try:
            url = app_config.ticketon_get_shows
            raw = redis_client.get(self.get_redis_for_shows_key(parameter))
            if raw is not None:
                dto = TicketonShowsRedisStore.model_validate_json(raw)
                if dto.last_updated + timedelta(minutes=app_config.ticketon_update_redis_in_minutes) > datetime.now() and dto.data.shows:
                    return dto.data
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"type[]={parameter.type}")
                params.append(f"place[]={parameter.place}")
                params.append(f"with[]={parameter.withParam}")
                params.append(f"i18n={parameter.i18n}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonShowsDataDTO.from_json(json_data)
                settle_data = TicketonShowsRedisStore(
                    query=parameter,
                    data=data,
                    last_updated=datetime.now(),
                )
                redis_client.setex(self.get_redis_for_shows_key(parameter), timedelta(minutes=app_config.ticketon_update_redis_in_minutes), settle_data.json())
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e

    async def get_ticketon_single_show(
            self, show_id: int, get_from_redis: bool = False
    ) -> TicketonSingleShowResponseDTO:
        try:
            cache_key = f"show_id_{show_id}"

            # 1. Проверяем в Redis
            if get_from_redis:
                cached = redis_client.get(cache_key)
                if cached:
                    try:
                        json_data = json.loads(cached)
                        return TicketonSingleShowResponseDTO.model_validate(json_data)
                    except Exception as e:
                        # если в кеше битые данные, просто идем в API
                        print(f"[WARN] Redis parse error: {e}")

            # 2. Идём в API
            url = app_config.ticketon_get_show
            params = [
                f"token={app_config.ticketon_api_key}",
                f"id={show_id}"
            ]
            url = f"{url}?{'&'.join(params)}"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()

            # 3. Парсим в DTO
            data = TicketonSingleShowResponseDTO.model_validate(json_data)

            # 4. Кладём в Redis (строкой, с TTL)
            redis_client.setex(
                cache_key,
                timedelta(minutes=app_config.ticketon_update_redis_in_minutes),
                json.dumps(json_data, ensure_ascii=False)
            )

            return data

        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Show ERROR: {str(e)}"
            ) from e


    async def get_ticketon_show_level(self,show_id:int,level_id:int)->TicketonShowLevelDTO:
        try:
            url = app_config.ticketon_show_level
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"id={show_id}")
                params.append(f"level={level_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonShowLevelDTO.from_json(json_data)
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e


    async def get_ticketon_get_level(self,level_id:int)->TicketonGetLevelDTO:
        try:
            url = app_config.ticketon_get_level
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"id={level_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonGetLevelDTO.from_json(json_data)
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e

    async def sale_ticketon(self,dto:TicketonBookingRequestDTO)->Union[TicketonBookingShowBookingDTO|TicketonBookingErrorResponseDTO]:
        try:
            url = app_config.ticketon_create_sale
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"lang={dto.lang}")
                params.append(f"show={dto.show}")
                for seat in dto.seats:
                    params.append("seats[]="+seat)
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                adapter = TypeAdapter(
                    Union[TicketonBookingShowBookingDTO, TicketonBookingErrorResponseDTO]
                )
                return adapter.validate_python(json_data)
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e


    async def get_ticketon_get_level(self,level_id:int)->TicketonGetLevelDTO:
        try:
            url = app_config.ticketon_get_level
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"id={level_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonGetLevelDTO.from_json(json_data)
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e


    async def sale_cancel(self,sale_id:str):
        try:
            url = app_config.ticketon_sale_cancel
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"sale={sale_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e

    async def sale_refund(self, sale_id: str) -> TicketonSaleRefundResponseDTO:
        """
        Отмена продажи билетов в системе Ticketon.
        
        Args:
            sale_id: Идентификатор продажи для отмены
            
        Returns:
            TicketonSaleRefundResponseDTO: Результат операции отмены
        """
        try:
            url = app_config.ticketon_sale_refund
            async with httpx.AsyncClient() as client:
                # Строим параметры для запроса отмены
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"sale={sale_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                
                # Создаем правильный DTO для ответа на возврат
                return TicketonSaleRefundResponseDTO(
                    status=json_data.get('status', 0),
                    error=json_data.get('error'),
                    code=json_data.get('code')
                )
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon sale refund ERROR: {str(e)}"
            ) from e

    async def sale_confirm(self,dto:TicketonConfirmSaleRequestDTO)->TicketonConfirmSaleResponseDTO:
        try:
            url = app_config.ticketon_sale_confirm
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"sale={dto.sale}")
                params.append(f"email={dto.email}")
                params.append(f"phone={dto.phone}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonConfirmSaleResponseDTO.model_validate(json_data)
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e


    def get_redis_for_shows_key(self,parameter:TicketonGetShowsParameterDTO)->str:
        return f"{parameter.type}_{parameter.place}_{parameter.withParam}_{parameter.i18n}"






