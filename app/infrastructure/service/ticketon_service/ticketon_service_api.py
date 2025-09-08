from datetime import timedelta, datetime

import httpx

from app.adapters.dto.ticketon.ticketon_city_dto import TicketonCityDTO
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


    async def get_ticketon_single_show(self,show_id:int)->TicketonSingleShowResponseDTO:
        try:
            url = app_config.ticketon_get_show
            async with httpx.AsyncClient() as client:
                # Строим параметры как список строк
                params = []
                params.append(f"token={app_config.ticketon_api_key}")
                params.append(f"id={show_id}")
                # Собираем финальный URL
                url = f"{url}?{'&'.join(params)}"
                response = await client.get(url)
                response.raise_for_status()
                json_data = response.json()
                data = TicketonSingleShowResponseDTO.from_json(json_data)
                return data
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"Ticketon GET Shows ERROR: {str(e)}"
            ) from e


    def get_redis_for_shows_key(self,parameter:TicketonGetShowsParameterDTO)->str:
        return f"{parameter.type}_{parameter.place}_{parameter.withParam}_{parameter.i18n}"





