from datetime import date, datetime

from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon.ticketon_city_dto import TicketonCityDTO
from app.entities import CityEntity, CountryEntity
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class CitySeeder(BaseSeeder):
    def __int__(self):
        self.ticketon_cities:list[TicketonCityDTO] = []
        self.country_id = 112
    async def seed(self, session: AsyncSession) -> None:
        count_query = select(func.count()).select_from(CityEntity)
        total_items = await session.scalar(count_query)
        country_count_query = select(func.count()).select_from(CountryEntity)
        country_total_items = await session.scalar(country_count_query)
        if total_items > 0 or country_total_items == 0:
            cities = []
        else:
            country_query = (
                select(CountryEntity.id)
                .where(func.upper(CountryEntity.sota_code) == "KZ")
            )

            result = await session.execute(country_query)
            country_id = result.scalar_one_or_none()
            if country_id is not None:
                self.country_id = country_id
            service = TicketonServiceAPI()
            self.ticketon_cities = await service.get_ticketon_cities()
            cities = self.get_dev_data()
        await self.load_seeders(CityEntity, session, AppTableNames.CityTableName, cities)

    def get_dev_data(self) -> list[CityEntity]:
        cities = []
        for city in self.ticketon_cities:
            if city.tag is not None:
                if len(city.tag) > 0:
                    cities.append(
                        CityEntity(
                            country_id = self.country_id,
                            title_ru=city.name,
                            title_kk=city.name_kz,
                            title_en=city.name_en,
                            ticketon_city_id=city.city_id,
                            ticketon_tag=city.tag,
                        )
                    )
        return cities

    def get_prod_data(self) -> list[CityEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
