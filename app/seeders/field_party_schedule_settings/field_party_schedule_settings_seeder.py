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
            # Настройки для Поля А - Большое футбольное (party_id=1)
            FieldPartyScheduleSettingsEntity(
                id=1,
                party_id=1,
                active_start_at=date(2025, 12, 8),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],  # праздничные дни
                working_time=[
                    {"day":1,"start": "08:00", "end": "22:00"},
                    {"day":2,"start": "08:00", "end": "22:00"},
                    {"day":3,"start": "08:00", "end": "22:00"},
                    {"day":4,"start": "08:00", "end": "22:00"},
                    {"day":5,"start": "08:00", "end": "22:00"},
                    {"day":6,"start": "08:00", "end": "22:00"},
                    {"day":7,"start": "08:00", "end": "18:00"},
                ],
                break_time=[
                    {"day":1,"start": "12:00", "end": "13:00"},
                    {"day":1,"start": "19:00", "end": "19:30"},
                    {"day":2,"start": "12:00", "end": "13:00"},
                    {"day":3,"start": "12:00", "end": "13:00"},
                    {"day":4,"start": "12:00", "end": "13:00"},
                    {"day":5,"start": "12:00", "end": "13:00"},
                    {"day":6,"start": "12:00", "end": "13:00"},
                    {"day":7,"start": "12:00", "end": "13:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "12:00", "price": 25000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 30000},
                    {"day":1,"start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 2, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 2, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 2, "start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 3, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 3, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 3, "start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 4, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 4, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 4, "start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 5, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 5, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 5, "start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 6, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 6, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 6, "start": "18:00", "end": "22:00", "price": 35000},
                    {"day": 7, "start": "08:00", "end": "12:00", "price": 25000},
                    {"day": 7, "start": "12:00", "end": "18:00", "price": 30000},
                    {"day": 7, "start": "18:00", "end": "22:00", "price": 35000},
                ],
                session_minute_int=90,  # 90 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),
            
            # Настройки для Поля Б - Тренировочное (party_id=2)
            FieldPartyScheduleSettingsEntity(
                id=2,
                party_id=2,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "09:00", "end": "21:00"},
                    {"day":2,"start": "09:00", "end": "21:00"},
                    {"day":3,"start": "09:00", "end": "21:00"},
                    {"day":4,"start": "09:00", "end": "21:00"},
                    {"day":5,"start": "09:00", "end": "21:00"},
                    {"day":6,"start": "09:00", "end": "21:00"},
                    {"day":7,"start": "09:00", "end": "21:00"},
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
                    {"day":1,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":1,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":2,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":2,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":3,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":3,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":4,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":4,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":5,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":5,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":6,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":6,"start": "18:00", "end": "21:00", "price": 22000},
                    {"day":7,"start": "09:00", "end": "12:00", "price": 15000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 18000},
                    {"day":7,"start": "18:00", "end": "21:00", "price": 22000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=10,  # 10 минут перерыв
                booked_limit=4,  # максимум 4 бронирования подряд
            ),

            # Настройки для Поля 1 - Мини-футбол (party_id=3)
            FieldPartyScheduleSettingsEntity(
                id=3,
                party_id=3,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "07:00", "end": "23:00"},
                    {"day":2,"start": "07:00", "end": "23:00"},
                    {"day":3,"start": "07:00", "end": "23:00"},
                    {"day":4,"start": "07:00", "end": "23:00"},
                    {"day":5,"start": "07:00", "end": "23:00"},
                    {"day":6,"start": "07:00", "end": "23:00"},
                    {"day":7,"start": "07:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "12:00", "end": "12:30"},
                    {"day":1,"start": "20:00", "end": "20:30"},
                    {"day":2,"start": "12:00", "end": "12:30"},
                    {"day":2,"start": "20:00", "end": "20:30"},
                    {"day":3,"start": "12:00", "end": "12:30"},
                    {"day":3,"start": "20:00", "end": "20:30"},
                    {"day":4,"start": "12:00", "end": "12:30"},
                    {"day":4,"start": "20:00", "end": "20:30"},
                    {"day":5,"start": "12:00", "end": "12:30"},
                    {"day":5,"start": "20:00", "end": "20:30"},
                    {"day":6,"start": "12:00", "end": "12:30"},
                    {"day":6,"start": "20:00", "end": "20:30"},
                    {"day":7,"start": "12:00", "end": "12:30"},
                    {"day":7,"start": "20:00", "end": "20:30"},
                ],
                price_per_time=[
                    {"day":1,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":1,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":1,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":2,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":2,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":3,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":3,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":4,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":4,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":5,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":5,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":6,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":6,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":7,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":7,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 15000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),

            # Настройки для Поля 2 - Мини-футбол (party_id=4)
            FieldPartyScheduleSettingsEntity(
                id=4,
                party_id=4,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "07:00", "end": "23:00"},
                    {"day":2,"start": "07:00", "end": "23:00"},
                    {"day":3,"start": "07:00", "end": "23:00"},
                    {"day":4,"start": "07:00", "end": "23:00"},
                    {"day":5,"start": "07:00", "end": "23:00"},
                    {"day":6,"start": "07:00", "end": "23:00"},
                    {"day":7,"start": "07:00", "end": "23:00"},
                ],
                break_time=[
                    {"day":1,"start": "12:00", "end": "12:30"},
                    {"day":1,"start": "20:00", "end": "20:30"},
                    {"day":2,"start": "12:00", "end": "12:30"},
                    {"day":2,"start": "20:00", "end": "20:30"},
                    {"day":3,"start": "12:00", "end": "12:30"},
                    {"day":3,"start": "20:00", "end": "20:30"},
                    {"day":4,"start": "12:00", "end": "12:30"},
                    {"day":4,"start": "20:00", "end": "20:30"},
                    {"day":5,"start": "12:00", "end": "12:30"},
                    {"day":5,"start": "20:00", "end": "20:30"},
                    {"day":6,"start": "12:00", "end": "12:30"},
                    {"day":6,"start": "20:00", "end": "20:30"},
                    {"day":7,"start": "12:00", "end": "12:30"},
                    {"day":7,"start": "20:00", "end": "20:30"},
                ],
                price_per_time=[
                    {"day":1,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":1,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":1,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":2,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":2,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":3,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":3,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":4,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":4,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":5,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":5,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":6,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":6,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 15000},
                    {"day":7,"start": "07:00", "end": "10:00", "price": 8000},
                    {"day":7,"start": "10:00", "end": "18:00", "price": 12000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 15000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),

            # Настройки для Зала А - Мини-футбол (party_id=5)
            FieldPartyScheduleSettingsEntity(
                id=5,
                party_id=5,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "22:00"},
                    {"day":2,"start": "08:00", "end": "22:00"},
                    {"day":3,"start": "08:00", "end": "22:00"},
                    {"day":4,"start": "08:00", "end": "22:00"},
                    {"day":5,"start": "08:00", "end": "22:00"},
                    {"day":6,"start": "08:00", "end": "22:00"},
                    {"day":7,"start": "08:00", "end": "22:00"},
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
                    {"day":1,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":1,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":2,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":3,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":4,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":5,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":6,"start": "18:00", "end": "22:00", "price": 18000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 15000},
                    {"day":7,"start": "18:00", "end": "22:00", "price": 18000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=10,  # 10 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),

            # Настройки для Зала Б - Баскетбол (party_id=6)
            FieldPartyScheduleSettingsEntity(
                id=6,
                party_id=6,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "22:00"},
                    {"day":2,"start": "08:00", "end": "22:00"},
                    {"day":3,"start": "08:00", "end": "22:00"},
                    {"day":4,"start": "08:00", "end": "22:00"},
                    {"day":5,"start": "08:00", "end": "22:00"},
                    {"day":6,"start": "08:00", "end": "22:00"},
                    {"day":7,"start": "08:00", "end": "22:00"},
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
                    {"day":1,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":1,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":2,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":3,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":4,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":5,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":6,"start": "18:00", "end": "22:00", "price": 20000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 16000},
                    {"day":7,"start": "18:00", "end": "22:00", "price": 20000},
                ],
                session_minute_int=90,  # 90 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),

            # Настройки для Основного поля (party_id=7)
            FieldPartyScheduleSettingsEntity(
                id=7,
                party_id=7,
                active_start_at=date(2025, 3, 1),  # с марта по ноябрь (сезон)
                active_end_at=date(2025, 11, 30),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9)],
                working_time=[
                    {"day":1,"start": "09:00", "end": "21:00"},
                    {"day":2,"start": "09:00", "end": "21:00"},
                    {"day":3,"start": "09:00", "end": "21:00"},
                    {"day":4,"start": "09:00", "end": "21:00"},
                    {"day":5,"start": "09:00", "end": "21:00"},
                    {"day":6,"start": "09:00", "end": "21:00"},
                    {"day":7,"start": "09:00", "end": "21:00"},
                ],
                break_time=[
                    {"day":1,"start": "13:00", "end": "14:00"},
                    {"day":1,"start": "18:00", "end": "18:30"},
                    {"day":2,"start": "13:00", "end": "14:00"},
                    {"day":2,"start": "18:00", "end": "18:30"},
                    {"day":3,"start": "13:00", "end": "14:00"},
                    {"day":3,"start": "18:00", "end": "18:30"},
                    {"day":4,"start": "13:00", "end": "14:00"},
                    {"day":4,"start": "18:00", "end": "18:30"},
                    {"day":5,"start": "13:00", "end": "14:00"},
                    {"day":5,"start": "18:00", "end": "18:30"},
                    {"day":6,"start": "13:00", "end": "14:00"},
                    {"day":6,"start": "18:00", "end": "18:30"},
                    {"day":7,"start": "13:00", "end": "14:00"},
                    {"day":7,"start": "18:00", "end": "18:30"},
                ],
                price_per_time=[
                    {"day":1,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":1,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":2,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":2,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":3,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":3,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":4,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":4,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":5,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":5,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":6,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":6,"start": "18:00", "end": "21:00", "price": 30000},
                    {"day":7,"start": "09:00", "end": "12:00", "price": 20000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 25000},
                    {"day":7,"start": "18:00", "end": "21:00", "price": 30000},
                ],
                session_minute_int=90,  # 90 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=3,  # максимум 3 бронирования подряд
            ),

            # Настройки для Тренировочного поля №1 (party_id=8)
            FieldPartyScheduleSettingsEntity(
                id=8,
                party_id=8,
                active_start_at=date(2025, 3, 1),  # с марта по ноябрь (сезон)
                active_end_at=date(2025, 11, 30),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "20:00"},
                    {"day":2,"start": "08:00", "end": "20:00"},
                    {"day":3,"start": "08:00", "end": "20:00"},
                    {"day":4,"start": "08:00", "end": "20:00"},
                    {"day":5,"start": "08:00", "end": "20:00"},
                    {"day":6,"start": "08:00", "end": "20:00"},
                    {"day":7,"start": "08:00", "end": "20:00"},
                ],
                break_time=[
                    {"day":1,"start": "12:00", "end": "13:00"},
                    {"day":2,"start": "12:00", "end": "13:00"},
                    {"day":3,"start": "12:00", "end": "13:00"},
                    {"day":4,"start": "12:00", "end": "13:00"},
                    {"day":5,"start": "12:00", "end": "13:00"},
                    {"day":6,"start": "12:00", "end": "13:00"},
                    {"day":7,"start": "12:00", "end": "13:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":1,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":1,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":2,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":2,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":3,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":3,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":4,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":4,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":5,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":5,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":6,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":6,"start": "16:00", "end": "20:00", "price": 18000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 12000},
                    {"day":7,"start": "12:00", "end": "16:00", "price": 15000},
                    {"day":7,"start": "16:00", "end": "20:00", "price": 18000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=10,  # 10 минут перерыв
                booked_limit=4,  # максимум 4 бронирования подряд
            ),

            # Настройки для Зала мини-футбола (party_id=9)
            FieldPartyScheduleSettingsEntity(
                id=9,
                party_id=9,
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
                    {"day":1,"start": "14:00", "end": "15:00"},
                    {"day":2,"start": "14:00", "end": "15:00"},
                    {"day":3,"start": "14:00", "end": "15:00"},
                    {"day":4,"start": "14:00", "end": "15:00"},
                    {"day":5,"start": "14:00", "end": "15:00"},
                    {"day":6,"start": "14:00", "end": "15:00"},
                    {"day":7,"start": "14:00", "end": "15:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":1,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":2,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":3,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":4,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":5,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":6,"start": "18:00", "end": "23:00", "price": 16000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 9000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":7,"start": "18:00", "end": "23:00", "price": 16000},
                ],
                session_minute_int=60,  # 60 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),

            # Настройки для Баскетбольного зала (party_id=10)
            FieldPartyScheduleSettingsEntity(
                id=10,
                party_id=10,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "22:00"},
                    {"day":2,"start": "08:00", "end": "22:00"},
                    {"day":3,"start": "08:00", "end": "22:00"},
                    {"day":4,"start": "08:00", "end": "22:00"},
                    {"day":5,"start": "08:00", "end": "22:00"},
                    {"day":6,"start": "08:00", "end": "22:00"},
                    {"day":7,"start": "08:00", "end": "22:00"},
                ],
                break_time=[
                    {"day":1,"start": "14:00", "end": "15:00"},
                    {"day":2,"start": "14:00", "end": "15:00"},
                    {"day":3,"start": "14:00", "end": "15:00"},
                    {"day":4,"start": "14:00", "end": "15:00"},
                    {"day":5,"start": "14:00", "end": "15:00"},
                    {"day":6,"start": "14:00", "end": "15:00"},
                    {"day":7,"start": "14:00", "end": "15:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":1,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":2,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":3,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":4,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":5,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":6,"start": "18:00", "end": "22:00", "price": 17000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 11000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 14000},
                    {"day":7,"start": "18:00", "end": "22:00", "price": 17000},
                ],
                session_minute_int=90,  # 90 минут сессия
                break_between_session_int=15,  # 15 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),

            # Настройки для Волейбольного зала (party_id=11)
            FieldPartyScheduleSettingsEntity(
                id=11,
                party_id=11,
                active_start_at=date(2025, 1, 1),
                active_end_at=date(2025, 12, 31),
                working_days=[1, 2, 3, 4, 5, 6, 7],  # каждый день
                excluded_dates=[date(2025, 5, 1), date(2025, 5, 9), date(2025, 12, 31)],
                working_time=[
                    {"day":1,"start": "08:00", "end": "22:00"},
                    {"day":2,"start": "08:00", "end": "22:00"},
                    {"day":3,"start": "08:00", "end": "22:00"},
                    {"day":4,"start": "08:00", "end": "22:00"},
                    {"day":5,"start": "08:00", "end": "22:00"},
                    {"day":6,"start": "08:00", "end": "22:00"},
                    {"day":7,"start": "08:00", "end": "22:00"},
                ],
                break_time=[
                    {"day":1,"start": "14:00", "end": "15:00"},
                    {"day":2,"start": "14:00", "end": "15:00"},
                    {"day":3,"start": "14:00", "end": "15:00"},
                    {"day":4,"start": "14:00", "end": "15:00"},
                    {"day":5,"start": "14:00", "end": "15:00"},
                    {"day":6,"start": "14:00", "end": "15:00"},
                    {"day":7,"start": "14:00", "end": "15:00"},
                ],
                price_per_time=[
                    {"day":1,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":1,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":1,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":2,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":2,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":2,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":3,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":3,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":3,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":4,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":4,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":4,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":5,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":5,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":5,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":6,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":6,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":6,"start": "18:00", "end": "22:00", "price": 16000},
                    {"day":7,"start": "08:00", "end": "12:00", "price": 10000},
                    {"day":7,"start": "12:00", "end": "18:00", "price": 13000},
                    {"day":7,"start": "18:00", "end": "22:00", "price": 16000},
                ],
                session_minute_int=90,  # 90 минут сессия
                break_between_session_int=10,  # 10 минут перерыв
                booked_limit=2,  # максимум 2 бронирования подряд
            ),
        ]

    def get_prod_data(self) -> list[FieldPartyScheduleSettingsEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass