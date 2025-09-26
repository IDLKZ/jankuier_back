from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import FieldPartyEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class FieldPartySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        field_parties = self.get_data()
        await self.load_seeders(
            FieldPartyEntity, session, AppTableNames.FieldPartyTableName, field_parties
        )

    def get_dev_data(self) -> list[FieldPartyEntity]:
        return [
            # Поле №1 (отдельно стоящее) - field_id=1
            FieldPartyEntity(
                id=1,
                image_id=None,
                field_id=1,
                title_ru="Поле №1 - Мини-футбол",
                title_kk="№1 алаң - Мини-футбол",
                title_en="Field #1 - Mini Football",
                value=DbValueConstants.get_value("Поле №1 - Мини-футбол"),
                person_qty=12,  # 5×5 и 6×6
                length_m=40,
                width_m=20,
                deepth_m=None,
                latitude="43.238253",
                longitude="76.889709",
                is_active=True,
                is_covered=False,  # уличное поле
                is_default=True,
                cover_type=0,  # без покрытия, искусственный газон
            ),

            # Поле №2 (в комплексе из двух соседних полей) - field_id=1
            FieldPartyEntity(
                id=2,
                image_id=None,
                field_id=1,
                title_ru="Поле №2 - Мини-футбол",
                title_kk="№2 алаң - Мини-футбол",
                title_en="Field #2 - Mini Football",
                value=DbValueConstants.get_value("Поле №2 - Мини-футбол"),
                person_qty=12,  # 5×5 и 6×6
                length_m=40,
                width_m=20,
                deepth_m=None,
                latitude="43.238353",
                longitude="76.889809",
                is_active=True,
                is_covered=False,  # уличное поле
                is_default=False,
                cover_type=0,  # без покрытия, искусственный газон
            ),

            # Поле №3 (соседнее с Полем №2) - field_id=1
            FieldPartyEntity(
                id=3,
                image_id=None,
                field_id=1,
                title_ru="Поле №3 - Мини-футбол",
                title_kk="№3 алаң - Мини-футбол",
                title_en="Field #3 - Mini Football",
                value=DbValueConstants.get_value("Поле №3 - Мини-футбол"),
                person_qty=12,  # 5×5 и 6×6
                length_m=40,
                width_m=20,
                deepth_m=None,
                latitude="43.238453",
                longitude="76.889909",
                is_active=True,
                is_covered=False,  # уличное поле
                is_default=False,
                cover_type=0,  # без покрытия, искусственный газон
            ),

            # Крытый футбольный манеж (105 × 68 м поле стандарт FIFA 11×11) - field_id=1
            FieldPartyEntity(
                id=4,
                image_id=None,
                field_id=1,
                title_ru="Крытый футбольный манеж FIFA",
                title_kk="FIFA жабық футбол манежі",
                title_en="FIFA Indoor Football Arena",
                value=DbValueConstants.get_value("Крытый футбольный манеж FIFA"),
                person_qty=22,  # 11×11
                length_m=105,
                width_m=68,
                deepth_m=8,  # высота манежа
                latitude="43.238153",
                longitude="76.889609",
                is_active=True,
                is_covered=True,  # крытое помещение
                is_default=False,
                cover_type=2,  # крытый зал
            ),
        ]

    def get_prod_data(self) -> list[FieldPartyEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass