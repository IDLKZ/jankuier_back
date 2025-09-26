from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import FieldEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class FieldSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        fields = self.get_data()
        await self.load_seeders(
            FieldEntity, session, AppTableNames.FieldTableName, fields
        )

    def get_dev_data(self) -> list[FieldEntity]:
        return [
            FieldEntity(
                id=1,
                image_id=None,
                city_id=1,  # Алматы
                title_ru="Футбольный комплекс Бауыржан Момышулы",
                title_kk="Бауыржан Момышұлы футбол кешені",
                title_en="Baurzhan Momyshuly Football Complex",
                description_ru="Современный футбольный комплекс с уличными мини-футбольными полями и крытым манежем FIFA стандарта",
                description_kk="Көшедегі мини-футбол алаңдары мен FIFA стандартындағы жабық манежі бар заманауи футбол кешені",
                description_en="Modern football complex with outdoor mini football fields and FIFA standard indoor arena",
                value=DbValueConstants.get_value("Футбольный комплекс Бауыржан Момышулы"),
                address_ru="ул. Бауыржана Момышулы, 5а, Алматы",
                address_kk="Бауыржан Момышұлы көшесі, 5а, Алматы",
                address_en="Baurzhan Momyshuly Street, 5a, Almaty",
                latitude="43.238253",
                longitude="76.889709",
                is_active=True,
                has_cover=True,  # есть крытый манеж
                phone="+77051234567",
                additional_phone="+77051234568",
                email="info@baurzhan-football.kz",
                whatsapp="+77051234567",
                telegram="@baurzhan_football",
                instagram="@baurzhan_football_kz",
                tiktok="@baurzhan_football",
            ),
        ]

    def get_prod_data(self) -> list[FieldEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass