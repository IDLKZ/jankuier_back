import httpx

from app.adapters.dto.ticketon.ticketon_city_dto import TicketonCityDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config


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

