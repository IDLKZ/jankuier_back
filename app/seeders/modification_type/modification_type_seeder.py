from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ModificationTypeEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ModificationTypeSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        modification_types = self.get_data()
        await self.load_seeders(
            ModificationTypeEntity, session, AppTableNames.ModificationTypeTableName, modification_types
        )

    def get_dev_data(self) -> list[ModificationTypeEntity]:
        return [
            ModificationTypeEntity(
                id=1,
                title_ru="Размер",
                title_kk="Өлшемі",
                title_en="Size",
                value=DbValueConstants.get_value("Размер"),
            ),
            ModificationTypeEntity(
                id=2,
                title_ru="Цвет",
                title_kk="Түсі",
                title_en="Color",
                value=DbValueConstants.get_value("Цвет"),
            ),
            ModificationTypeEntity(
                id=3,
                title_ru="Материал",
                title_kk="Материал",
                title_en="Material",
                value=DbValueConstants.get_value("Материал"),
            ),
            ModificationTypeEntity(
                id=4,
                title_ru="Бренд",
                title_kk="Бренд",
                title_en="Brand",
                value=DbValueConstants.get_value("Бренд"),
            ),
            ModificationTypeEntity(
                id=5,
                title_ru="Вес",
                title_kk="Салмақ",
                title_en="Weight",
                value=DbValueConstants.get_value("Вес"),
            ),
            ModificationTypeEntity(
                id=6,
                title_ru="Пол",
                title_kk="Жыныс",
                title_en="Gender",
                value=DbValueConstants.get_value("Пол"),
            ),
            ModificationTypeEntity(
                id=7,
                title_ru="Возрастная группа",
                title_kk="Жас тобы",
                title_en="Age Group",
                value=DbValueConstants.get_value("Возрастная группа"),
            ),
            ModificationTypeEntity(
                id=8,
                title_ru="Сезон",
                title_kk="Маусым",
                title_en="Season",
                value=DbValueConstants.get_value("Сезон"),
            ),
        ]

    def get_prod_data(self) -> list[ModificationTypeEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass