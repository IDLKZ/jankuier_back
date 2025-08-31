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
                city_id=1,  # Можно потом привязать к конкретному городу
                title_ru="Стадион Централь",
                title_kk="Централь стадионы",
                title_en="Central Stadium",
                description_ru="Современный многофункциональный стадион с несколькими полями для различных видов спорта",
                description_kk="Әртүрлі спорт түрлеріне арналған бірнеше алаңдары бар заманауи көпфункционалды стадион",
                description_en="Modern multifunctional stadium with several fields for various sports",
                value=DbValueConstants.get_value("Стадион Централь"),
                address_ru="ул. Абая, 150, Алматы",
                address_kk="Абай көшесі, 150, Алматы",
                address_en="Abai Street, 150, Almaty",
                latitude="43.238253",
                longitude="76.889709",
                is_active=True,
                has_cover=True,
                phone="+77051234567",
                additional_phone="+77051234568",
                email="info@central-stadium.kz",
                whatsapp="+77051234567",
                telegram="@central_stadium",
                instagram="@central_stadium_kz",
                tiktok="@central_stadium",
            ),
            FieldEntity(
                id=2,
                image_id=None,
                city_id=2,
                title_ru="Спорткомплекс Жастар",
                title_kk="Жастар спорт кешені",
                title_en="Youth Sports Complex",
                description_ru="Спортивный комплекс для молодежи с современными футбольными полями",
                description_kk="Заманауи футбол алаңдары бар жастарға арналған спорт кешені",
                description_en="Sports complex for youth with modern football fields",
                value=DbValueConstants.get_value("Спорткомплекс Жастар"),
                address_ru="пр. Достык, 234, Алматы",
                address_kk="Достық даңғылы, 234, Алматы",
                address_en="Dostyk Avenue, 234, Almaty",
                latitude="43.220150",
                longitude="76.851350",
                is_active=True,
                has_cover=False,
                phone="+77052345678",
                additional_phone=None,
                email="contact@youth-complex.kz",
                whatsapp="+77052345678",
                telegram=None,
                instagram="@youth_complex",
                tiktok=None,
            ),
            FieldEntity(
                id=3,
                image_id=None,
                city_id=3,
                title_ru="Арена Спорт",
                title_kk="Спорт Аренасы",
                title_en="Sports Arena",
                description_ru="Крытая спортивная арена с универсальными полями для различных игр",
                description_kk="Әртүрлі ойындарға арналған әмбебап алаңдары бар жабық спорт аренасы",
                description_en="Indoor sports arena with universal fields for various games",
                value=DbValueConstants.get_value("Арена Спорт"),
                address_ru="ул. Сатпаева, 90/1, Алматы",
                address_kk="Сәтпаев көшесі, 90/1, Алматы",
                address_en="Satpaev Street, 90/1, Almaty",
                latitude="43.245680",
                longitude="76.908450",
                is_active=True,
                has_cover=True,
                phone="+77053456789",
                additional_phone="+77053456790",
                email="booking@sports-arena.kz",
                whatsapp="+77053456789",
                telegram="@sports_arena_kz",
                instagram="@sports_arena",
                tiktok="@sportsarena_kz",
            ),
            FieldEntity(
                id=4,
                image_id=None,
                city_id=1,
                title_ru="Футбольная академия Кайрат",
                title_kk="Қайрат футбол академиясы",
                title_en="Kairat Football Academy",
                description_ru="Профессиональная футбольная академия с тренировочными полями высокого качества",
                description_kk="Жоғары сапалы жаттығу алаңдары бар кәсіби футбол академиясы",
                description_en="Professional football academy with high-quality training fields",
                value=DbValueConstants.get_value("Футбольная академия Кайрат"),
                address_ru="ул. Толе би, 59, Алматы",
                address_kk="Төле би көшесі, 59, Алматы",
                address_en="Tole bi Street, 59, Almaty",
                latitude="43.256420",
                longitude="76.928340",
                is_active=True,
                has_cover=False,
                phone="+77054567890",
                additional_phone=None,
                email="academy@kairat.kz",
                whatsapp="+77054567890",
                telegram=None,
                instagram="@kairat_academy",
                tiktok=None,
            ),
            FieldEntity(
                id=5,
                image_id=None,
                city_id=4,
                title_ru="Многофункциональный центр Алатау",
                title_kk="Алатау көпфункционалды орталығы",
                title_en="Alatau Multifunctional Center",
                description_ru="Современный центр с полями для мини-футбола, баскетбола и волейбола",
                description_kk="Мини-футбол, баскетбол және волейболға арналған алаңдары бар заманауи орталық",
                description_en="Modern center with fields for mini-football, basketball and volleyball",
                value=DbValueConstants.get_value("Многофункциональный центр Алатау"),
                address_ru="мкр. Алатау, ул. Жетысу, 10, Алматы",
                address_kk="Алатау ш/а, Жетісу көшесі, 10, Алматы",
                address_en="Alatau district, Zhetysu Street, 10, Almaty",
                latitude="43.160890",
                longitude="76.820450",
                is_active=True,
                has_cover=True,
                phone="+77055678901",
                additional_phone="+77055678902",
                email="info@alatau-center.kz",
                whatsapp="+77055678901",
                telegram="@alatau_center",
                instagram="@alatau_sports",
                tiktok="@alatauspots",
            ),
        ]

    def get_prod_data(self) -> list[FieldEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass