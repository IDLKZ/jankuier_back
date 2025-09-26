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
                city_id=1,  # Алматы
                title_ru="Футбольная академия Бауыржан Момышулы",
                title_kk="Бауыржан Момышұлы футбол академиясы",
                title_en="Baurzhan Momyshuly Football Academy",
                description_ru="Профессиональная футбольная академия при спорткомплексе Бауыржан Момышулы. Подготовка юных футболистов по международным стандартам FIFA с использованием современных методик тренировок.",
                description_kk="Бауыржан Момышұлы спорт кешеніндегі кәсіби футбол академиясы. FIFA халықаралық стандарттары бойынша жас футболшыларды заманауи жаттығу әдістемелерін қолдана отырып дайындау.",
                description_en="Professional football academy at Baurzhan Momyshuly sports complex. Training young footballers to FIFA international standards using modern training methodologies.",
                value=DbValueConstants.get_value("Футбольная академия Бауыржан Момышулы"),
                address_ru="ул. Бауыржана Момышулы, 5а, Алматы",
                address_kk="Бауыржан Момышұлы көшесі, 5а, Алматы",
                address_en="Baurzhan Momyshuly Street, 5a, Almaty",
                working_time=[
                    {"day": 1, "start": "15:00", "end": "21:00"},  # Понедельник
                    {"day": 2, "start": "15:00", "end": "21:00"},  # Вторник
                    {"day": 3, "start": "15:00", "end": "21:00"},  # Среда
                    {"day": 4, "start": "15:00", "end": "21:00"},  # Четверг
                    {"day": 5, "start": "15:00", "end": "21:00"},  # Пятница
                    {"day": 6, "start": "09:00", "end": "18:00"},  # Суббота
                    {"day": 7, "start": "09:00", "end": "18:00"}   # Воскресенье
                ],
                is_active=True,
                gender=0,  # для всех полов
                min_age=5,
                max_age=18,
                average_price=Decimal("18000.00"),
                average_training_time_in_minute=90,
                phone="+77051234567",
                additional_phone="+77051234568",
                email="academy@baurzhan-football.kz",
                whatsapp="+77051234567",
                telegram="@baurzhan_football_academy",
                instagram="@baurzhan_football_academy",
                tik_tok="@baurzhan_football",
                site="https://baurzhan-football.kz/academy",
            ),
            AcademyEntity(
                id=2,
                image_id=None,
                city_id=1,  # Алматы
                title_ru="Футбольная школа Кайрат",
                title_kk="Қайрат футбол мектебі",
                title_en="Kairat Football School",
                description_ru="Легендарная футбольная школа ФК Кайрат с 50-летней историей. Воспитала множество звезд казахстанского и международного футбола. Академия полного цикла от детских групп до молодежной команды.",
                description_kk="ФК Қайраттың 50 жылдық тарихы бар аfsanалы футбол мектебі. Қазақстандық және халықаралық футболдың көптеген жұлдыздарын тәрбиелеген. Балалар топтарынан жастар командасына дейінгі толық циклды академия.",
                description_en="Legendary Kairat FC football school with 50 years of history. Has raised many stars of Kazakhstani and international football. Full cycle academy from children's groups to youth team.",
                value=DbValueConstants.get_value("Футбольная школа Кайрат"),
                address_ru="ул. Толе би, 59, Алматы",
                address_kk="Төле би көшесі, 59, Алматы",
                address_en="Tole bi Street, 59, Almaty",
                working_time=[
                    {"day": 1, "start": "14:00", "end": "20:00"},
                    {"day": 2, "start": "14:00", "end": "20:00"},
                    {"day": 3, "start": "14:00", "end": "20:00"},
                    {"day": 4, "start": "14:00", "end": "20:00"},
                    {"day": 5, "start": "14:00", "end": "20:00"},
                    {"day": 6, "start": "08:00", "end": "18:00"},
                    {"day": 7, "start": "08:00", "end": "18:00"}
                ],
                is_active=True,
                gender=0,  # для всех полов
                min_age=6,
                max_age=19,
                average_price=Decimal("22000.00"),
                average_training_time_in_minute=105,
                phone="+77054567890",
                additional_phone="+77054567891",
                email="academy@kairat.kz",
                whatsapp="+77054567890",
                telegram="@kairat_academy",
                instagram="@kairat_football_academy",
                tik_tok="@kairat_academy",
                site="https://kairat.kz/academy",
            ),
            AcademyEntity(
                id=3,
                image_id=None,
                city_id=1,  # Алматы
                title_ru="Детская футбольная академия Алматы",
                title_kk="Алматы балалар футбол академиясы",
                title_en="Almaty Children's Football Academy",
                description_ru="Современная детская футбольная академия, специализирующаяся на начальной подготовке юных футболистов. Особое внимание уделяется техническим навыкам и интеллектуальному развитию игроков.",
                description_kk="Жас футболшылардың бастапқы дайындығына маманданған заманауи балалар футбол академиясы. Ойыншылардың техникалық дағдылары мен зияткерлік дамуына ерекше көңіл бөлінеді.",
                description_en="Modern children's football academy specializing in initial training of young footballers. Special attention is paid to technical skills and intellectual development of players.",
                value=DbValueConstants.get_value("Детская футбольная академия Алматы"),
                address_ru="пр. Достык, 234, Алматы",
                address_kk="Достық даңғылы, 234, Алматы",
                address_en="Dostyk Avenue, 234, Almaty",
                working_time=[
                    {"day": 1, "start": "16:00", "end": "20:00"},
                    {"day": 2, "start": "16:00", "end": "20:00"},
                    {"day": 3, "start": "16:00", "end": "20:00"},
                    {"day": 4, "start": "16:00", "end": "20:00"},
                    {"day": 5, "start": "16:00", "end": "20:00"},
                    {"day": 6, "start": "10:00", "end": "17:00"},
                    {"day": 7, "start": "10:00", "end": "17:00"}
                ],
                is_active=True,
                gender=0,  # для всех полов
                min_age=4,
                max_age=16,
                average_price=Decimal("15000.00"),
                average_training_time_in_minute=75,
                phone="+77052345678",
                additional_phone=None,
                email="info@almaty-football.kz",
                whatsapp="+77052345678",
                telegram="@almaty_football_academy",
                instagram="@almaty_children_football",
                tik_tok="@almaty_football",
                site="https://almaty-football.kz",
            ),
            AcademyEntity(
                id=4,
                image_id=None,
                city_id=2,  # Алматы
                title_ru="Школа футбола Астана",
                title_kk="Астана футбол мектебі",
                title_en="Astana Football School",
                description_ru="Филиал знаменитой школы ФК Астана в Алматы. Готовит футболистов по лучшим европейским методикам с привлечением иностранных тренеров. Сильная физическая и психологическая подготовка.",
                description_kk="Алматыдағы атақты ФК Астана мектебінің филиалы. Шетелдік жаттықтырушыларды тарта отырып, ең жақсы еуропалық әдістемелер бойынша футболшыларды дайындайды. Күшті физикалық және психологиялық дайындық.",
                description_en="Branch of the famous FC Astana school in Almaty. Trains footballers using the best European methodologies with foreign coaches. Strong physical and psychological preparation.",
                value=DbValueConstants.get_value("Школа футбола Астана"),
                address_ru="ул. Сатпаева, 90/1, Алматы",
                address_kk="Сәтпаев көшесі, 90/1, Алматы",
                address_en="Satpaev Street, 90/1, Almaty",
                working_time=[
                    {"day": 1, "start": "15:30", "end": "21:30"},
                    {"day": 2, "start": "15:30", "end": "21:30"},
                    {"day": 3, "start": "15:30", "end": "21:30"},
                    {"day": 4, "start": "15:30", "end": "21:30"},
                    {"day": 5, "start": "15:30", "end": "21:30"},
                    {"day": 6, "start": "09:00", "end": "19:00"},
                    {"day": 7, "start": "09:00", "end": "19:00"}
                ],
                is_active=True,
                gender=1,  # преимущественно мальчики (но не исключительно)
                min_age=7,
                max_age=20,
                average_price=Decimal("25000.00"),
                average_training_time_in_minute=120,
                phone="+77053456789",
                additional_phone="+77053456790",
                email="almaty@astana-football.kz",
                whatsapp="+77053456789",
                telegram="@astana_football_almaty",
                instagram="@astana_football_school",
                tik_tok="@astana_football",
                site="https://astana-football.kz/almaty",
            ),
            AcademyEntity(
                id=5,
                image_id=None,
                city_id=1,  # Алматы
                title_ru="Женская футбольная академия Алматы",
                title_kk="Алматы әйелдер футбол академиясы",
                title_en="Almaty Women's Football Academy",
                description_ru="Первая специализированная женская футбольная академия в Казахстане. Развивает женский футбол, готовит игроков для национальной сборной и профессиональных клубов. Современный подход к тренировкам девочек и женщин.",
                description_kk="Қазақстандағы алғашқы мамандандырылған әйелдер футбол академиясы. Әйелдер футболын дамытады, ұлттық құрама және кәсіби клубтарға ойыншыларды дайындайды. Қыздар мен әйелдерді жаттықтыруға заманауи көзқарас.",
                description_en="First specialized women's football academy in Kazakhstan. Develops women's football, prepares players for national team and professional clubs. Modern approach to training girls and women.",
                value=DbValueConstants.get_value("Женская футбольная академия Алматы"),
                address_ru="мкр. Алатау, ул. Жетысу, 10, Алматы",
                address_kk="Алатау ш/а, Жетісу көшесі, 10, Алматы",
                address_en="Alatau district, Zhetysu Street, 10, Almaty",
                working_time=[
                    {"day": 1, "start": "16:30", "end": "20:30"},
                    {"day": 2, "start": "16:30", "end": "20:30"},
                    {"day": 3, "start": "16:30", "end": "20:30"},
                    {"day": 4, "start": "16:30", "end": "20:30"},
                    {"day": 5, "start": "16:30", "end": "20:30"},
                    {"day": 6, "start": "10:30", "end": "17:30"},
                    {"day": 7, "start": "10:30", "end": "17:30"}
                ],
                is_active=True,
                gender=2,  # только девочки/женщины
                min_age=5,
                max_age=25,
                average_price=Decimal("16000.00"),
                average_training_time_in_minute=90,
                phone="+77055678901",
                additional_phone="+77055678902",
                email="info@women-football-almaty.kz",
                whatsapp="+77055678901",
                telegram="@almaty_women_football",
                instagram="@almaty_women_football",
                tik_tok="@women_football_almaty",
                site="https://women-football-almaty.kz",
            ),
        ]

    def get_prod_data(self) -> list[AcademyEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass