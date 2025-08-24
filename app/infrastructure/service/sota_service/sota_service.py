import asyncio
from typing import Dict

import httpx

from app.adapters.dto.sota.sota_auth_token_dto import SotaTokenDTO
from app.adapters.dto.sota.sota_country_dto import SotaCountryListDTO, SotaCountryDTO
from app.adapters.dto.sota.sota_sport_dto import SotaSportDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.service.redis_service import RedisService


class SotaService:

    def __init__(self):
        self.sota_access_token = "sota_access_token"
        self.redis_service = RedisService()

    async def get_sota_token(self)->str:
        token = self.redis_service.get_sota_token(self.sota_access_token)
        if token is None:
            params = {
                "email": app_config.sota_auth_email,
                "password": app_config.sota_auth_password
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(app_config.sota_auth_api, data=params)
                    data:SotaTokenDTO = SotaTokenDTO.parse_obj(response.json())
                    self.redis_service.set_sota_token(self.sota_access_token,data.access)
                    response.raise_for_status()
                    return data.access
                except Exception as e:
                    raise AppExceptionResponse.internal_error(
                        message=f"SOTA GET AUTH TOKEN ERROR: {str(e)}"  # noqa:RUF010,RUF100,
                    ) from e
        else:
            return token

    async def get_countries_all_languages(self) -> list[SotaCountryDTO]:
        token = await self.get_sota_token()
        url = app_config.sota_get_country_api
        params = {
            "page": 1,
            "page_size": 300
        }

        async def fetch_lang(lang: str, client: httpx.AsyncClient) -> tuple[
            Dict[int, str], Dict[int, str], Dict[int, str]]:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept-Language": lang
            }
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                return (
                    {item["id"]: item["name"] for item in json_data.get("results", [])},
                    {item["id"]: item.get("flag_image") for item in json_data.get("results", [])},
                    {item["id"]: item.get("code") for item in json_data.get("results", [])},
                )
            except Exception as e:
                raise AppExceptionResponse.internal_error(
                    message=f"SOTA GET COUNTRIES [{lang.upper()}] ERROR: {str(e)}"
                ) from e

        try:
            async with httpx.AsyncClient() as client:
                ru_names, ru_flags, ru_codes = await fetch_lang("ru", client)
                kk_names, _, _ = await fetch_lang("kk", client)
                en_names, _, _ = await fetch_lang("en", client)

            result = []
            for country_id in ru_names:
                result.append(SotaCountryDTO(
                    id=country_id,
                    name_ru=ru_names[country_id],
                    name_kk=kk_names.get(country_id),
                    name_en=en_names.get(country_id),
                    flag_image=ru_flags.get(country_id),
                    code=ru_codes.get(country_id),
                ))

            return result

        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET COUNTRIES MULTI-LANG ERROR: {str(e)}"
            ) from e

    from typing import Dict, Optional
    import httpx

    async def get_sport_types(self) -> list[SotaSportDTO]:
        token = await self.get_sota_token()
        url = app_config.sota_get_sports_api  # исправлено

        params = {
            "page": 1,
            "page_size": 300
        }

        async def fetch_lang(lang: str, client: httpx.AsyncClient) -> Dict[int, str]:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept-Language": lang
            }
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                return {
                    item["id"]: item["name"]
                    for item in json_data.get("results", [])
                }, {
                    item["id"]: item.get("created_at")
                    for item in json_data.get("results", [])
                }, {
                    item["id"]: item.get("updated_at")
                    for item in json_data.get("results", [])
                }, {
                    item["id"]: item.get("game_timer_type")
                    for item in json_data.get("results", [])
                }
            except Exception as e:
                raise AppExceptionResponse.internal_error(
                    message=f"SOTA GET SPORTS [{lang.upper()}] ERROR: {str(e)}"
                ) from e

        try:
            async with httpx.AsyncClient() as client:
                ru_names, ru_created, ru_updated, ru_timer = await fetch_lang("ru", client)
                kk_names, _, _, _ = await fetch_lang("kk", client)
                en_names, _, _, _ = await fetch_lang("en", client)

            result = []
            for sport_id in ru_names:
                result.append(SotaSportDTO(
                    id=sport_id,
                    created_at=ru_created.get(sport_id),
                    updated_at=ru_updated.get(sport_id),
                    name_ru=ru_names.get(sport_id),
                    name_kk=kk_names.get(sport_id),
                    name_en=en_names.get(sport_id),
                    game_timer_type=ru_timer.get(sport_id)
                ))

            return result

        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"SOTA GET SPORTS MULTI-LANG ERROR: {str(e)}"
            ) from e



