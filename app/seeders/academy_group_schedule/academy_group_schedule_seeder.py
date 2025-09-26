from datetime import date, time, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import AcademyGroupScheduleEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class AcademyGroupScheduleSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        schedules = self.get_data()
        await self.load_seeders(
            AcademyGroupScheduleEntity, session, AppTableNames.AcademyGroupScheduleTableName, schedules
        )

    def get_dev_data(self) -> list[AcademyGroupScheduleEntity]:
        return [
            # Расписание для группы "Малыши 5-6 лет" (group_id=1) - Академия Бауыржан Момышулы
            AcademyGroupScheduleEntity(
                id=1,
                group_id=1,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(16, 0),  # 16:00
                end_at=time(16, 45),   # 16:45
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=2,
                group_id=1,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(16, 0),
                end_at=time(16, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=3,
                group_id=1,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(10, 0),
                end_at=time(10, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юные футболисты 7-9 лет" (group_id=2)
            AcademyGroupScheduleEntity(
                id=4,
                group_id=2,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(17, 0),
                end_at=time(18, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=5,
                group_id=2,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(11, 0),
                end_at=time(12, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Школьники 10-12 лет" (group_id=3)
            AcademyGroupScheduleEntity(
                id=6,
                group_id=3,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(18, 30),
                end_at=time(20, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=7,
                group_id=3,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(14, 0),
                end_at=time(15, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Подростки 13-15 лет" (group_id=4)
            AcademyGroupScheduleEntity(
                id=8,
                group_id=4,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(19, 0),
                end_at=time(20, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=9,
                group_id=4,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(16, 0),
                end_at=time(17, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юниоры 16-18 лет" (group_id=5)
            AcademyGroupScheduleEntity(
                id=10,
                group_id=5,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(20, 0),
                end_at=time(22, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=11,
                group_id=5,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(20, 0),
                end_at=time(22, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Кайрат U-8 (6-8 лет)" (group_id=6) - Школа Кайрат
            AcademyGroupScheduleEntity(
                id=12,
                group_id=6,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(15, 30),
                end_at=time(16, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=13,
                group_id=6,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(9, 0),
                end_at=time(10, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Кайрат U-12 (9-12 лет)" (group_id=7)
            AcademyGroupScheduleEntity(
                id=14,
                group_id=7,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(17, 30),
                end_at=time(19, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=15,
                group_id=7,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(11, 0),
                end_at=time(12, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Кайрат U-16 (13-16 лет)" (group_id=8)
            AcademyGroupScheduleEntity(
                id=16,
                group_id=8,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(18, 0),
                end_at=time(20, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=17,
                group_id=8,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(18, 0),
                end_at=time(20, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=18,
                group_id=8,
                training_date=date(2025, 10, 6),  # понедельник
                start_at=time(18, 0),
                end_at=time(20, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Кайрат U-19 (17-19 лет)" (group_id=9)
            AcademyGroupScheduleEntity(
                id=19,
                group_id=9,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(19, 30),
                end_at=time(21, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=20,
                group_id=9,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(15, 0),
                end_at=time(17, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Первые шаги 4-5 лет" (group_id=10) - Детская академия Алматы
            AcademyGroupScheduleEntity(
                id=21,
                group_id=10,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(16, 30),
                end_at=time(17, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=22,
                group_id=10,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(11, 0),
                end_at=time(11, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Базовая техника 6-9 лет" (group_id=11)
            AcademyGroupScheduleEntity(
                id=23,
                group_id=11,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=24,
                group_id=11,
                training_date=date(2025, 10, 6),  # понедельник
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юные таланты 10-13 лет" (group_id=12)
            AcademyGroupScheduleEntity(
                id=25,
                group_id=12,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(18, 30),
                end_at=time(19, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=26,
                group_id=12,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(13, 0),
                end_at=time(14, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Подготовка к взрослому футболу 14-16 лет" (group_id=13)
            AcademyGroupScheduleEntity(
                id=27,
                group_id=13,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(19, 0),
                end_at=time(20, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Астана U-10 (7-10 лет)" (group_id=14) - Школа Астана
            AcademyGroupScheduleEntity(
                id=28,
                group_id=14,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(16, 30),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=29,
                group_id=14,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(10, 0),
                end_at=time(11, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Астана U-14 (11-14 лет)" (group_id=15)
            AcademyGroupScheduleEntity(
                id=30,
                group_id=15,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(17, 30),
                end_at=time(19, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=31,
                group_id=15,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(17, 30),
                end_at=time(19, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Астана U-18 (15-18 лет)" (group_id=16)
            AcademyGroupScheduleEntity(
                id=32,
                group_id=16,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(19, 0),
                end_at=time(21, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=33,
                group_id=16,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(16, 0),
                end_at=time(18, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Астана молодежь 19-20 лет" (group_id=17)
            AcademyGroupScheduleEntity(
                id=34,
                group_id=17,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(20, 0),
                end_at=time(22, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=35,
                group_id=17,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(18, 0),
                end_at=time(20, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Девочки-малышки 5-7 лет" (group_id=18) - Женская академия
            AcademyGroupScheduleEntity(
                id=36,
                group_id=18,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=37,
                group_id=18,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(11, 30),
                end_at=time(12, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юные футболистки 8-12 лет" (group_id=19)
            AcademyGroupScheduleEntity(
                id=38,
                group_id=19,
                training_date=date(2025, 10, 2),  # четверг
                start_at=time(17, 30),
                end_at=time(18, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=39,
                group_id=19,
                training_date=date(2025, 10, 4),  # суббота
                start_at=time(12, 0),
                end_at=time(13, 15),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Девочки-подростки 13-16 лет" (group_id=20)
            AcademyGroupScheduleEntity(
                id=40,
                group_id=20,
                training_date=date(2025, 10, 1),  # среда
                start_at=time(18, 0),
                end_at=time(19, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=41,
                group_id=20,
                training_date=date(2025, 10, 6),  # понедельник
                start_at=time(18, 0),
                end_at=time(19, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Молодые женщины 17-25 лет" (group_id=21) с одним переносом
            AcademyGroupScheduleEntity(
                id=42,
                group_id=21,
                training_date=date(2025, 10, 3),  # пятница
                start_at=time(19, 0),
                end_at=time(20, 45),
                reschedule_start_at=datetime(2025, 10, 4, 19, 30),  # перенесено на субботу 19:30
                reschedule_end_at=datetime(2025, 10, 4, 21, 15),   # до 21:15
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=43,
                group_id=21,
                training_date=date(2025, 10, 5),  # воскресенье
                start_at=time(16, 0),
                end_at=time(17, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
        ]

    def get_prod_data(self) -> list[AcademyGroupScheduleEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass