from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import AcademyEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class AcademySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        academies = self.get_data()
        await self.load_seeders(
            AcademyEntity, session, AppTableNames.AcademyTableName, academies
        )

    def get_dev_data(self) -> list[AcademyEntity]:
        return [
            AcademyEntity(
                id=1,
                image_id=None,
                city_id=None,  # Можно потом привязать к конкретному городу
                title_ru="Футбольная академия Кайрат",
                title_kk="Қайрат футбол академиясы",
                title_en="Kairat Football Academy",
                description_ru="Профессиональная футбольная академия с многолетней историей. Подготовка юных футболистов по современным методикам.",
                description_kk="Көпжылдық тарихы бар кәсіби футбол академиясы. Заманауи әдістемелер бойынша жас футболшыларды дайындау.",
                description_en="Professional football academy with years of experience. Training young footballers using modern methodologies.",
                value=DbValueConstants.get_value("Футбольная академия Кайрат"),
                address_ru="ул. Толе би, 59, Алматы",
                address_kk="Төле би көшесі, 59, Алматы",
                address_en="Tole bi Street, 59, Almaty",
                working_time=[
                    {"day": "monday", "start": "08:00", "end": "20:00"},
                    {"day": "tuesday", "start": "08:00", "end": "20:00"},
                    {"day": "wednesday", "start": "08:00", "end": "20:00"},
                    {"day": "thursday", "start": "08:00", "end": "20:00"},
                    {"day": "friday", "start": "08:00", "end": "20:00"},
                    {"day": "saturday", "start": "09:00", "end": "18:00"},
                    {"day": "sunday", "start": "09:00", "end": "18:00"}
                ],
                is_active=True,
                gender=0,  # для всех
                min_age=6,
                max_age=18,
                average_price=Decimal("15000.00"),
                average_training_time_in_minute=90,
                phone="+77054567890",
                additional_phone="+77054567891",
                email="academy@kairat.kz",
                whatsapp="+77054567890",
                telegram="@kairat_academy",
                instagram="@kairat_academy",
                tik_tok="@kairat_academy",
                site="https://kairat.kz/academy",
            ),
            AcademyEntity(
                id=2,
                image_id=None,
                city_id=None,
                title_ru="Баскетбольная академия Астана Тайгерс",
                title_kk="Астана Тайгерс баскетбол академиясы",
                title_en="Astana Tigers Basketball Academy",
                description_ru="Ведущая баскетбольная академия Казахстана. Обучение основам игры и профессиональная подготовка.",
                description_kk="Қазақстанның жетекші баскетбол академиясы. Ойын негіздерін үйрету және кәсіби дайындық.",
                description_en="Leading basketball academy in Kazakhstan. Teaching game fundamentals and professional training.",
                value=DbValueConstants.get_value("Баскетбольная академия Астана Тайгерс"),
                address_ru="пр. Аль-Фараби, 77, Алматы",
                address_kk="Әл-Фараби даңғылы, 77, Алматы",
                address_en="Al-Farabi Avenue, 77, Almaty",
                working_time=[
                    {"day": "monday", "start": "15:00", "end": "21:00"},
                    {"day": "tuesday", "start": "15:00", "end": "21:00"},
                    {"day": "wednesday", "start": "15:00", "end": "21:00"},
                    {"day": "thursday", "start": "15:00", "end": "21:00"},
                    {"day": "friday", "start": "15:00", "end": "21:00"},
                    {"day": "saturday", "start": "10:00", "end": "18:00"},
                    {"day": "sunday", "start": "10:00", "end": "18:00"}
                ],
                is_active=True,
                gender=0,  # для всех
                min_age=8,
                max_age=20,
                average_price=Decimal("12000.00"),
                average_training_time_in_minute=120,
                phone="+77051234567",
                additional_phone=None,
                email="info@tigers-academy.kz",
                whatsapp="+77051234567",
                telegram="@tigers_academy",
                instagram="@astana_tigers_academy",
                tik_tok="@tigers_academy",
                site="https://astana-tigers.kz",
            ),
            AcademyEntity(
                id=3,
                image_id=None,
                city_id=None,
                title_ru="Теннисная академия Тенис Клуб",
                title_kk="Теннис Клуб теннис академиясы",
                title_en="Tennis Club Academy",
                description_ru="Современная теннисная академия с крытыми и открытыми кортами. Индивидуальные и групповые занятия.",
                description_kk="Жабық және ашық корттары бар заманауи теннис академиясы. Жеке және топтық сабақтар.",
                description_en="Modern tennis academy with indoor and outdoor courts. Individual and group lessons.",
                value=DbValueConstants.get_value("Теннисная академия Тенис Клуб"),
                address_ru="ул. Назарбаева, 223, Алматы",
                address_kk="Назарбаев көшесі, 223, Алматы",
                address_en="Nazarbayev Street, 223, Almaty",
                working_time=[
                    {"day": "monday", "start": "07:00", "end": "22:00"},
                    {"day": "tuesday", "start": "07:00", "end": "22:00"},
                    {"day": "wednesday", "start": "07:00", "end": "22:00"},
                    {"day": "thursday", "start": "07:00", "end": "22:00"},
                    {"day": "friday", "start": "07:00", "end": "22:00"},
                    {"day": "saturday", "start": "08:00", "end": "21:00"},
                    {"day": "sunday", "start": "08:00", "end": "21:00"}
                ],
                is_active=True,
                gender=0,  # для всех
                min_age=5,
                max_age=50,
                average_price=Decimal("18000.00"),
                average_training_time_in_minute=60,
                phone="+77052345678",
                additional_phone="+77052345679",
                email="tennis@club-academy.kz",
                whatsapp="+77052345678",
                telegram="@tennis_club_academy",
                instagram="@tennis_club_almaty",
                tik_tok=None,
                site="https://tennis-club.kz",
            ),
            AcademyEntity(
                id=4,
                image_id=None,
                city_id=None,
                title_ru="Плавательная школа Дельфин",
                title_kk="Дельфин жүзу мектебі",
                title_en="Dolphin Swimming School",
                description_ru="Профессиональная школа плавания для детей и взрослых. Обучение всем стилям плавания.",
                description_kk="Балалар мен ересектерге арналған кәсіби жүзу мектебі. Барлық жүзу стильдерін үйрету.",
                description_en="Professional swimming school for children and adults. Teaching all swimming styles.",
                value=DbValueConstants.get_value("Плавательная школа Дельфин"),
                address_ru="ул. Абылай хана, 105, Алматы",
                address_kk="Абылай хан көшесі, 105, Алматы",
                address_en="Abylai Khan Street, 105, Almaty",
                working_time=[
                    {"day": "monday", "start": "06:00", "end": "22:00"},
                    {"day": "tuesday", "start": "06:00", "end": "22:00"},
                    {"day": "wednesday", "start": "06:00", "end": "22:00"},
                    {"day": "thursday", "start": "06:00", "end": "22:00"},
                    {"day": "friday", "start": "06:00", "end": "22:00"},
                    {"day": "saturday", "start": "08:00", "end": "20:00"},
                    {"day": "sunday", "start": "08:00", "end": "20:00"}
                ],
                is_active=True,
                gender=0,  # для всех
                min_age=3,
                max_age=60,
                average_price=Decimal("10000.00"),
                average_training_time_in_minute=45,
                phone="+77053456789",
                additional_phone=None,
                email="info@dolphin-swim.kz",
                whatsapp="+77053456789",
                telegram="@dolphin_swim",
                instagram="@dolphin_swimming_school",
                tik_tok="@dolphin_swim",
                site="https://dolphin-swim.kz",
            ),
            AcademyEntity(
                id=5,
                image_id=None,
                city_id=None,
                title_ru="Академия единоборств Барыс",
                title_kk="Барыс жекпе-жек академиясы",
                title_en="Barys Martial Arts Academy",
                description_ru="Комплексная подготовка по различным видам единоборств: карате, тхэквондо, дзюдо.",
                description_kk="Әртүрлі жекпе-жек түрлері бойынша кешенді дайындық: каратэ, тхэквондо, дзюдо.",
                description_en="Comprehensive training in various martial arts: karate, taekwondo, judo.",
                value=DbValueConstants.get_value("Академия единоборств Барыс"),
                address_ru="ул. Жандосова, 140, Алматы",
                address_kk="Жандосов көшесі, 140, Алматы",
                address_en="Zhandosov Street, 140, Almaty",
                working_time=[
                    {"day": "monday", "start": "16:00", "end": "21:00"},
                    {"day": "tuesday", "start": "16:00", "end": "21:00"},
                    {"day": "wednesday", "start": "16:00", "end": "21:00"},
                    {"day": "thursday", "start": "16:00", "end": "21:00"},
                    {"day": "friday", "start": "16:00", "end": "21:00"},
                    {"day": "saturday", "start": "10:00", "end": "16:00"},
                    {"day": "sunday", "start": "10:00", "end": "16:00"}
                ],
                is_active=True,
                gender=1,  # только мальчики
                min_age=6,
                max_age=25,
                average_price=Decimal("8000.00"),
                average_training_time_in_minute=90,
                phone="+77055678901",
                additional_phone="+77055678902",
                email="academy@barys-fight.kz",
                whatsapp="+77055678901",
                telegram="@barys_academy",
                instagram="@barys_martial_arts",
                tik_tok="@barys_fight",
                site="https://barys-fight.kz",
            ),
            AcademyEntity(
                id=6,
                image_id=None,
                city_id=None,
                title_ru="Гимнастический центр Грация",
                title_kk="Грация гимнастика орталығы",
                title_en="Grace Gymnastics Center",
                description_ru="Художественная и спортивная гимнастика для девочек. Профессиональные тренеры и современное оборудование.",
                description_kk="Қыздарға арналған көркем және спорттық гимнастика. Кәсіби жаттықтырушылар және заманауи жабдық.",
                description_en="Rhythmic and artistic gymnastics for girls. Professional coaches and modern equipment.",
                value=DbValueConstants.get_value("Гимнастический центр Грация"),
                address_ru="мкр. Самал-2, д. 111, Алматы",
                address_kk="Самал-2 ш/а, 111-үй, Алматы",
                address_en="Samal-2 district, building 111, Almaty",
                working_time=[
                    {"day": "monday", "start": "15:00", "end": "20:00"},
                    {"day": "tuesday", "start": "15:00", "end": "20:00"},
                    {"day": "wednesday", "start": "15:00", "end": "20:00"},
                    {"day": "thursday", "start": "15:00", "end": "20:00"},
                    {"day": "friday", "start": "15:00", "end": "20:00"},
                    {"day": "saturday", "start": "09:00", "end": "17:00"},
                    {"day": "sunday", "start": "09:00", "end": "17:00"}
                ],
                is_active=True,
                gender=2,  # только девочки
                min_age=4,
                max_age=16,
                average_price=Decimal("14000.00"),
                average_training_time_in_minute=90,
                phone="+77056789012",
                additional_phone=None,
                email="info@grace-gym.kz",
                whatsapp="+77056789012",
                telegram="@grace_gymnastics",
                instagram="@grace_gymnastics_center",
                tik_tok="@grace_gym",
                site="https://grace-gymnastics.kz",
            ),
        ]

    def get_prod_data(self) -> list[AcademyEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass