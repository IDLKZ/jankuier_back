from datetime import date, datetime

from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sota.sota_country_dto import SotaCountryDTO
from app.entities import CountryEntity
from app.infrastructure.service.sota_service.sota_service import SotaService
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class CountrySeeder(BaseSeeder):
    def __int__(self):
        self.countries_sota:list[SotaCountryDTO] = []
    async def seed(self, session: AsyncSession) -> None:
        count_query = select(func.count()).select_from(CountryEntity)
        total_items = await session.scalar(count_query)
        if total_items > 0:
            countries = []
        else:
            service = SotaService()
            self.countries_sota = await service.get_countries_all_languages()
            countries = self.get_dev_data()
        await self.load_seeders(CountryEntity, session, AppTableNames.CountryTableName, countries)

    def get_dev_data(self) -> list[CountryEntity]:
        countries = []
        for country in self.countries_sota:
            if country.name_ru != "":
                countries.append(
                    CountryEntity(
                        id=country.id,
                        title_ru=country.name_ru,
                        title_kk=country.name_kk,
                        title_en=country.name_en,
                        sota_code=country.code,
                        sota_flag_image=country.flag_image,
                    )
                )
        return countries

    def get_prod_data(self) -> list[CountryEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
