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
            # Расписание для группы "Юные футболисты 6-8 лет" (group_id=1)
            AcademyGroupScheduleEntity(
                id=1,
                group_id=1,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(16, 0),  # 16:00
                end_at=time(17, 0),   # 17:00
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=2,
                group_id=1,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(16, 0),
                end_at=time(17, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=3,
                group_id=1,
                training_date=date(2025, 1, 10),  # пятница
                start_at=time(16, 0),
                end_at=time(17, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Футбол 9-12 лет" (group_id=2)
            AcademyGroupScheduleEntity(
                id=4,
                group_id=2,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(17, 30),
                end_at=time(19, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=5,
                group_id=2,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(17, 30),
                end_at=time(19, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=6,
                group_id=2,
                training_date=date(2025, 1, 11),  # суббота
                start_at=time(10, 0),
                end_at=time(11, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юниоры 13-16 лет" (group_id=3)
            AcademyGroupScheduleEntity(
                id=7,
                group_id=3,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(19, 0),
                end_at=time(21, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=8,
                group_id=3,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(19, 0),
                end_at=time(21, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Мини-баскет 8-10 лет" (group_id=4)
            AcademyGroupScheduleEntity(
                id=9,
                group_id=4,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(15, 30),
                end_at=time(17, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=10,
                group_id=4,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(15, 30),
                end_at=time(17, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Баскетбол 11-14 лет" (group_id=5)
            AcademyGroupScheduleEntity(
                id=11,
                group_id=5,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(17, 0),
                end_at=time(19, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=12,
                group_id=5,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(17, 0),
                end_at=time(19, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Молодежь 15-20 лет" (group_id=6)
            AcademyGroupScheduleEntity(
                id=13,
                group_id=6,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(19, 30),
                end_at=time(22, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=14,
                group_id=6,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(19, 30),
                end_at=time(22, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Теннис для начинающих 5-8 лет" (group_id=7)
            AcademyGroupScheduleEntity(
                id=15,
                group_id=7,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(16, 0),
                end_at=time(16, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=16,
                group_id=7,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(16, 0),
                end_at=time(16, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Юниорский теннис 9-14 лет" (group_id=8)
            AcademyGroupScheduleEntity(
                id=17,
                group_id=8,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=18,
                group_id=8,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=19,
                group_id=8,
                training_date=date(2025, 1, 10),  # пятница
                start_at=time(17, 0),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Груднички 3-5 лет" (group_id=9)
            AcademyGroupScheduleEntity(
                id=20,
                group_id=9,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(10, 0),
                end_at=time(10, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=21,
                group_id=9,
                training_date=date(2025, 1, 11),  # суббота
                start_at=time(10, 0),
                end_at=time(10, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Детское плавание 6-12 лет" (group_id=10)
            AcademyGroupScheduleEntity(
                id=22,
                group_id=10,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(17, 0),
                end_at=time(17, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=23,
                group_id=10,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(17, 0),
                end_at=time(17, 45),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Взрослые 18+" (group_id=11)
            AcademyGroupScheduleEntity(
                id=24,
                group_id=11,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(20, 0),
                end_at=time(21, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=25,
                group_id=11,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(20, 0),
                end_at=time(21, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=26,
                group_id=11,
                training_date=date(2025, 1, 10),  # пятница
                start_at=time(20, 0),
                end_at=time(21, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Карате 6-10 лет" (group_id=12)
            AcademyGroupScheduleEntity(
                id=27,
                group_id=12,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(16, 30),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=28,
                group_id=12,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(16, 30),
                end_at=time(18, 0),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Дзюдо 11-16 лет" (group_id=13) - с переносом
            AcademyGroupScheduleEntity(
                id=29,
                group_id=13,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(18, 30),
                end_at=time(20, 30),
                reschedule_start_at=datetime(2025, 1, 8, 19, 0),  # перенесено на среду 19:00
                reschedule_end_at=datetime(2025, 1, 8, 21, 0),   # до 21:00
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=30,
                group_id=13,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(18, 30),
                end_at=time(20, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Художественная гимнастика 4-7 лет" (group_id=14)
            AcademyGroupScheduleEntity(
                id=31,
                group_id=14,
                training_date=date(2025, 1, 6),  # понедельник
                start_at=time(15, 30),
                end_at=time(16, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=32,
                group_id=14,
                training_date=date(2025, 1, 8),  # среда
                start_at=time(15, 30),
                end_at=time(16, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=33,
                group_id=14,
                training_date=date(2025, 1, 10),  # пятница
                start_at=time(15, 30),
                end_at=time(16, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=False,
                is_finished=False,
            ),

            # Расписание для группы "Спортивная гимнастика 8-12 лет" (group_id=15) - одно занятие отменено
            AcademyGroupScheduleEntity(
                id=34,
                group_id=15,
                training_date=date(2025, 1, 7),  # вторник
                start_at=time(17, 0),
                end_at=time(18, 30),
                reschedule_start_at=None,
                reschedule_end_at=None,
                is_active=True,
                is_canceled=True,  # отменено
                is_finished=False,
            ),
            AcademyGroupScheduleEntity(
                id=35,
                group_id=15,
                training_date=date(2025, 1, 9),  # четверг
                start_at=time(17, 0),
                end_at=time(18, 30),
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