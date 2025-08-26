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
            # Участки для Стадиона Централь (field_id=1)
            FieldPartyEntity(
                id=1,
                image_id=None,
                field_id=1,
                title_ru="Поле А - Большое футбольное",
                title_kk="А алаңы - Үлкен футбол",
                title_en="Field A - Large Football",
                value=DbValueConstants.get_value("Поле А - Большое футбольное"),
                person_qty=22,  # 11 на 11
                length_m=105,
                width_m=68,
                deepth_m=None,
                latitude="43.238353",
                longitude="76.889809",
                is_active=True,
                is_covered=True,
                is_default=True,
                cover_type=1,  # полное покрытие
            ),
            FieldPartyEntity(
                id=2,
                image_id=None,
                field_id=1,
                title_ru="Поле Б - Тренировочное",
                title_kk="Б алаңы - Жаттығу",
                title_en="Field B - Training",
                value=DbValueConstants.get_value("Поле Б - Тренировочное"),
                person_qty=14,  # 7 на 7
                length_m=50,
                width_m=30,
                deepth_m=None,
                latitude="43.238153",
                longitude="76.889609",
                is_active=True,
                is_covered=True,
                is_default=False,
                cover_type=1,  # полное покрытие
            ),

            # Участки для Спорткомплекса Жастар (field_id=2)
            FieldPartyEntity(
                id=3,
                image_id=None,
                field_id=2,
                title_ru="Поле 1 - Мини-футбол",
                title_kk="1 алаң - Мини-футбол",
                title_en="Field 1 - Mini Football",
                value=DbValueConstants.get_value("Поле 1 - Мини-футбол"),
                person_qty=10,  # 5 на 5
                length_m=40,
                width_m=20,
                deepth_m=None,
                latitude="43.220250",
                longitude="76.851450",
                is_active=True,
                is_covered=False,
                is_default=True,
                cover_type=0,  # без покрытия
            ),
            FieldPartyEntity(
                id=4,
                image_id=None,
                field_id=2,
                title_ru="Поле 2 - Мини-футбол",
                title_kk="2 алаң - Мини-футбол",
                title_en="Field 2 - Mini Football",
                value=DbValueConstants.get_value("Поле 2 - Мини-футбол"),
                person_qty=10,  # 5 на 5
                length_m=40,
                width_m=20,
                deepth_m=None,
                latitude="43.220050",
                longitude="76.851250",
                is_active=True,
                is_covered=False,
                is_default=False,
                cover_type=0,  # без покрытия
            ),

            # Участки для Арены Спорт (field_id=3)
            FieldPartyEntity(
                id=5,
                image_id=None,
                field_id=3,
                title_ru="Зал А - Мини-футбол",
                title_kk="А залы - Мини-футбол",
                title_en="Hall A - Mini Football",
                value=DbValueConstants.get_value("Зал А - Мини-футбол"),
                person_qty=10,  # 5 на 5
                length_m=40,
                width_m=20,
                deepth_m=8,  # высота зала
                latitude="43.245780",
                longitude="76.908550",
                is_active=True,
                is_covered=True,
                is_default=True,
                cover_type=2,  # крытый зал
            ),
            FieldPartyEntity(
                id=6,
                image_id=None,
                field_id=3,
                title_ru="Зал Б - Баскетбол",
                title_kk="Б залы - Баскетбол",
                title_en="Hall B - Basketball",
                value=DbValueConstants.get_value("Зал Б - Баскетбол"),
                person_qty=10,  # 5 на 5
                length_m=28,
                width_m=15,
                deepth_m=8,  # высота зала
                latitude="43.245580",
                longitude="76.908350",
                is_active=True,
                is_covered=True,
                is_default=False,
                cover_type=2,  # крытый зал
            ),

            # Участки для Футбольной академии Кайрат (field_id=4)
            FieldPartyEntity(
                id=7,
                image_id=None,
                field_id=4,
                title_ru="Основное поле",
                title_kk="Негізгі алаң",
                title_en="Main Field",
                value=DbValueConstants.get_value("Основное поле"),
                person_qty=22,  # 11 на 11
                length_m=105,
                width_m=68,
                deepth_m=None,
                latitude="43.256520",
                longitude="76.928440",
                is_active=True,
                is_covered=False,
                is_default=True,
                cover_type=0,  # без покрытия
            ),
            FieldPartyEntity(
                id=8,
                image_id=None,
                field_id=4,
                title_ru="Тренировочное поле №1",
                title_kk="№1 жаттығу алаңы",
                title_en="Training Field #1",
                value=DbValueConstants.get_value("Тренировочное поле №1"),
                person_qty=14,  # 7 на 7
                length_m=60,
                width_m=40,
                deepth_m=None,
                latitude="43.256320",
                longitude="76.928240",
                is_active=True,
                is_covered=False,
                is_default=False,
                cover_type=0,  # без покрытия
            ),

            # Участки для Многофункционального центра Алатау (field_id=5)
            FieldPartyEntity(
                id=9,
                image_id=None,
                field_id=5,
                title_ru="Зал мини-футбола",
                title_kk="Мини-футбол залы",
                title_en="Mini Football Hall",
                value=DbValueConstants.get_value("Зал мини-футбола"),
                person_qty=10,  # 5 на 5
                length_m=40,
                width_m=20,
                deepth_m=7,  # высота зала
                latitude="43.160990",
                longitude="76.820550",
                is_active=True,
                is_covered=True,
                is_default=True,
                cover_type=2,  # крытый зал
            ),
            FieldPartyEntity(
                id=10,
                image_id=None,
                field_id=5,
                title_ru="Баскетбольный зал",
                title_kk="Баскетбол залы",
                title_en="Basketball Hall",
                value=DbValueConstants.get_value("Баскетбольный зал"),
                person_qty=10,  # 5 на 5
                length_m=28,
                width_m=15,
                deepth_m=7,  # высота зала
                latitude="43.160790",
                longitude="76.820350",
                is_active=True,
                is_covered=True,
                is_default=False,
                cover_type=2,  # крытый зал
            ),
            FieldPartyEntity(
                id=11,
                image_id=None,
                field_id=5,
                title_ru="Волейбольный зал",
                title_kk="Волейбол залы",
                title_en="Volleyball Hall",
                value=DbValueConstants.get_value("Волейбольный зал"),
                person_qty=12,  # 6 на 6
                length_m=18,
                width_m=9,
                deepth_m=7,  # высота зала
                latitude="43.160890",
                longitude="76.820250",
                is_active=True,
                is_covered=True,
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