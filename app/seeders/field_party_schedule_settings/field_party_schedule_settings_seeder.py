from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import FieldPartyScheduleSettingsEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class FieldPartyScheduleSettingsSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        settings = self.get_data()
        await self.load_seeders(
            FieldPartyScheduleSettingsEntity, session, AppTableNames.FieldPartyScheduleSettingsTableName, settings
        )

    def get_dev_data(self) -> list[FieldPartyScheduleSettingsEntity]:
        return [
            # Настройки для Поля №1 - Мини-футбол (party_id=1)
            FieldPartyScheduleSettingsEntity(
                id=1,
                party_id=1,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "23:00"},
                    {"day":2,"start": "08:00", "end": "23:00"},
                    {"day":3,"start": "08:00", "end": "23:00"},
                    {"day":4,"start": "08:00", "end": "23:00"},
                    {"day":5,"start": "08:00", "end": "23:00"},
                    {"day":6,"start": "08:00", "end": "23:00"},
                    {"day":7,"start": "08:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "13:00", "end": "14:00"},
                    {"day":2,"start": "13:00", "end": "14:00"},
                    {"day":3,"start": "13:00", "end": "14:00"},
                    {"day":4,"start": "13:00", "end": "14:00"},
                    {"day":5,"start": "13:00", "end": "14:00"},
                    {"day":6,"start": "13:00", "end": "14:00"},
                    {"day":7,"start": "13:00", "end": "14:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "18:00", "price": 15000},  # до 18:00
                    {"day":1,"start": "18:00", "end": "23:00", "price": 20000},  # после 18:00
                    {"day":2,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":3,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":4,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":5,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":6,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":7,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 20000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),

            # Настройки для Поля №2 - Мини-футбол (party_id=2)
            FieldPartyScheduleSettingsEntity(
                id=2,
                party_id=2,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "23:00"},
                    {"day":2,"start": "08:00", "end": "23:00"},
                    {"day":3,"start": "08:00", "end": "23:00"},
                    {"day":4,"start": "08:00", "end": "23:00"},
                    {"day":5,"start": "08:00", "end": "23:00"},
                    {"day":6,"start": "08:00", "end": "23:00"},
                    {"day":7,"start": "08:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "13:00", "end": "14:00"},
                    {"day":2,"start": "13:00", "end": "14:00"},
                    {"day":3,"start": "13:00", "end": "14:00"},
                    {"day":4,"start": "13:00", "end": "14:00"},
                    {"day":5,"start": "13:00", "end": "14:00"},
                    {"day":6,"start": "13:00", "end": "14:00"},
                    {"day":7,"start": "13:00", "end": "14:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "18:00", "price": 15000},  # до 18:00
                    {"day":1,"start": "18:00", "end": "23:00", "price": 20000},  # после 18:00
                    {"day":2,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":3,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":4,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":5,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":6,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":7,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 20000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),

            # Настройки для Поля №3 - Мини-футбол (party_id=3)
            FieldPartyScheduleSettingsEntity(
                id=3,
                party_id=3,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "23:00"},
                    {"day":2,"start": "08:00", "end": "23:00"},
                    {"day":3,"start": "08:00", "end": "23:00"},
                    {"day":4,"start": "08:00", "end": "23:00"},
                    {"day":5,"start": "08:00", "end": "23:00"},
                    {"day":6,"start": "08:00", "end": "23:00"},
                    {"day":7,"start": "08:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "13:00", "end": "14:00"},
                    {"day":2,"start": "13:00", "end": "14:00"},
                    {"day":3,"start": "13:00", "end": "14:00"},
                    {"day":4,"start": "13:00", "end": "14:00"},
                    {"day":5,"start": "13:00", "end": "14:00"},
                    {"day":6,"start": "13:00", "end": "14:00"},
                    {"day":7,"start": "13:00", "end": "14:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "18:00", "price": 15000},  # до 18:00
                    {"day":1,"start": "18:00", "end": "23:00", "price": 20000},  # после 18:00
                    {"day":2,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":3,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":4,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":5,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":6,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 20000},
                    {"day":7,"start": "08:00", "end": "18:00", "price": 15000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 20000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),

            # Настройки для Крытого футбольного манежа FIFA (party_id=4)
            FieldPartyScheduleSettingsEntity(
                id=4,
                party_id=4,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "23:00"},
                    {"day":2,"start": "08:00", "end": "23:00"},
                    {"day":3,"start": "08:00", "end": "23:00"},
                    {"day":4,"start": "08:00", "end": "23:00"},
                    {"day":5,"start": "08:00", "end": "23:00"},
                    {"day":6,"start": "08:00", "end": "23:00"},
                    {"day":7,"start": "08:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "12:00", "end": "13:00"},
                    {"day":1,"start": "15:00", "end": "16:00"},
                    {"day":2,"start": "12:00", "end": "13:00"},
                    {"day":2,"start": "15:00", "end": "16:00"},
                    {"day":3,"start": "12:00", "end": "13:00"},
                    {"day":3,"start": "15:00", "end": "16:00"},
                    {"day":4,"start": "12:00", "end": "13:00"},
                    {"day":4,"start": "15:00", "end": "16:00"},
                    {"day":5,"start": "12:00", "end": "13:00"},
                    {"day":5,"start": "15:00", "end": "16:00"},
                    {"day":6,"start": "12:00", "end": "13:00"},
                    {"day":6,"start": "15:00", "end": "16:00"},
                    {"day":7,"start": "12:00", "end": "13:00"},
                    {"day":7,"start": "15:00", "end": "16:00"},
                ],
                price_per_time=[
                    # Для ФЦ, СДЮШОР и детских школ специальные цены
                    {"day":1,"start": "08:00", "end": "12:00", "price": 60000},  # 08:00 – 12:00 — 60 000 тг/час
                    {"day":1,"start": "12:00", "end": "15:00", "price": 70000},  # 12:00 – 15:00 — 70 000 тг/час
                    {"day":1,"start": "15:00", "end": "23:00", "price": 100000}, # 15:00 – 23:00 — 100 000 тг/час
                    {"day":2,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":2,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":2,"start": "15:00", "end": "23:00", "price": 100000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":3,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":3,"start": "15:00", "end": "23:00", "price": 100000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":4,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":4,"start": "15:00", "end": "23:00", "price": 100000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":5,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":5,"start": "15:00", "end": "23:00", "price": 100000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":6,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":6,"start": "15:00", "end": "23:00", "price": 100000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 60000},
                    {"day":7,"start": "12:00", "end": "15:00", "price": 70000},
                    {"day":7,"start": "15:00", "end": "23:00", "price": 100000},
                ],
                session_minute_int=60,  # 60 минут сессия для больших полей обычно час
                break_between_session_int=30,  # 30 минут перерыв между большими играми
                booked_limit=2,  # максимум 2 бронирования подряд из-за высокой нагрузки
            ),
        ]

    def get_prod_data(self) -> list[FieldPartyScheduleSettingsEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass