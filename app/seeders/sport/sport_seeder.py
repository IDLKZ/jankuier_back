from slugify import slugify
from sqlalchemy import func,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.sota.sota_sport_dto import SotaSportDTO
from app.entities import SportEntity
from app.infrastructure.service.sota_service.sota_service import SotaService
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class SportSeeder(BaseSeeder):
    def __int__(self):
        self.sport_types:list[SotaSportDTO] = []
    async def seed(self, session: AsyncSession) -> None:
        count_query = select(func.count()).select_from(SportEntity)
        total_items = await session.scalar(count_query)
        if total_items > 0:
            sports = []
        else:
            service = SotaService()
            self.sport_types = await service.get_sport_types()
            sports = self.get_dev_data()
        await self.load_seeders(SportEntity, session, AppTableNames.SportTableName, sports)

    def get_dev_data(self) -> list[SportEntity]:
        sports = []
        for sport_type in self.sport_types:
            sports.append(
                SportEntity(
                    id=sport_type.id,
                    title_ru=sport_type.name_ru,
                    title_kk=sport_type.name_kk,
                    title_en=sport_type.name_en,
                    value=slugify(sport_type.name_ru, separator="_"),
                )
            )
        return sports

    def get_prod_data(self) -> list[SportEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
