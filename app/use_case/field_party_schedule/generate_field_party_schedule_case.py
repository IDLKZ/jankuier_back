from datetime import datetime, date, time, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.use_case.base_case import BaseUseCase
from app.entities.field_party_schedule_entity import FieldPartyScheduleEntity
from app.entities.field_party_schedule_settings_entity import FieldPartyScheduleSettingsEntity
from app.adapters.repository.base_repository import BaseRepository
from app.adapters.dto.field_party_schedule_settings.schedule_generator_dto import (
    ScheduleGeneratorResponseDTO,
    ScheduleRecordDTO
)
from app.core.app_exception_response import AppExceptionResponse


class GenerateFieldPartyScheduleCase(BaseUseCase[ScheduleGeneratorResponseDTO]):
    """UseCase для генерации расписания поля на основе настроек."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.schedule_repository = BaseRepository(FieldPartyScheduleEntity, db)
        self.settings_repository = BaseRepository(FieldPartyScheduleSettingsEntity, db)

    async def execute(self, party_id: int, regenerate_existing: bool = False) -> ScheduleGeneratorResponseDTO:
        """
        Генерирует расписание для поля на основе настроек.
        
        Args:
            party_id: ID партии поля
            regenerate_existing: Перегенерировать существующие записи
        """
        await self.validate(party_id=party_id)
        
        # Получаем настройки расписания
        settings = await self._get_settings_for_party(party_id)
        if not settings:
            return ScheduleGeneratorResponseDTO(
                success=False,
                message="Настройки расписания для данной партии поля не найдены",
                generated_count=0,
                schedule_records=[]
            )
        
        # Очищаем существующие записи при необходимости
        if regenerate_existing:
            await self._clear_existing_schedules(party_id, settings.id)
        
        # Генерируем слоты
        generated_slots = await self._generate_schedule_slots(settings)
        
        # Сохраняем сгенерированные слоты
        saved_records = await self._save_schedule_records(generated_slots)
        
        return ScheduleGeneratorResponseDTO(
            success=True,
            message=f"Успешно сгенерировано {len(saved_records)} слотов расписания",
            generated_count=len(saved_records),
            schedule_records=saved_records
        )

    async def validate(self, party_id: int) -> None:
        """Валидация входных параметров."""
        if party_id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID партии поля должен быть больше нуля"
            )

    async def _get_settings_for_party(self, party_id: int) -> FieldPartyScheduleSettingsEntity | None:
        """Получает активные настройки расписания для партии поля."""
        filters = [
            FieldPartyScheduleSettingsEntity.party_id == party_id,
            FieldPartyScheduleSettingsEntity.deleted_at.is_(None)
        ]
        results = await self.settings_repository.get_all(filters=filters)
        return results[0] if results else None

    async def _clear_existing_schedules(self, party_id: int, setting_id: int) -> None:
        """Удаляет существующие записи расписания."""
        delete_query = delete(FieldPartyScheduleEntity).where(
            FieldPartyScheduleEntity.party_id == party_id,
            FieldPartyScheduleEntity.setting_id == setting_id
        )
        await self.db.execute(delete_query)
        await self.db.commit()

    async def _generate_schedule_slots(self, settings: FieldPartyScheduleSettingsEntity) -> List[dict]:
        """
        Генерирует слоты расписания на основе настроек.
        
        Логика:
        1. Берём период active_start_at → active_end_at
        2. Фильтруем по дням недели (working_days)
        3. Пропускаем даты из excluded_dates
        4. Для каждого дня генерируем сессии на основе working_time
        5. Разрезаем на слоты по session_minute_int
        6. Добавляем перерывы break_between_session_int
        7. Убираем слоты, пересекающиеся с break_time
        8. Назначаем цену из price_per_time
        """
        slots = []
        
        # Получаем все рабочие дни в диапазоне
        working_dates = self._get_working_dates(
            settings.active_start_at,
            settings.active_end_at,
            settings.working_days,
            settings.excluded_dates
        )
        
        for work_date in working_dates:
            # Генерируем слоты для каждого дня
            daily_slots = self._generate_daily_slots(
                work_date=work_date,
                working_time=settings.working_time,
                break_time=settings.break_time or [],
                session_duration_minutes=settings.session_minute_int,
                break_between_sessions_minutes=settings.break_between_session_int,
                price_per_time=settings.price_per_time,
                party_id=settings.party_id,
                setting_id=settings.id
            )
            slots.extend(daily_slots)
        
        return slots

    def _get_working_dates(
        self, 
        start_date: date, 
        end_date: date, 
        working_days: List[int], 
        excluded_dates: List[date] | None
    ) -> List[date]:
        """Получает список рабочих дат в диапазоне."""
        working_dates = []
        current_date = start_date
        
        # excluded_dates уже содержит объекты datetime.date
        excluded_dates_set = set(excluded_dates) if excluded_dates else set()
        
        while current_date <= end_date:
            # Проверяем день недели (1=понедельник, 7=воскресенье)
            weekday = current_date.isoweekday()
            
            if weekday in working_days and current_date not in excluded_dates_set:
                working_dates.append(current_date)
            
            current_date += timedelta(days=1)
        
        return working_dates

    def _generate_daily_slots(
        self,
        work_date: date,
        working_time: List[dict],
        break_time: List[dict],
        session_duration_minutes: int,
        break_between_sessions_minutes: int,
        price_per_time: List[dict],
        party_id: int,
        setting_id: int
    ) -> List[dict]:
        """Генерирует слоты для одного рабочего дня."""
        daily_slots = []
        
        for work_period in working_time:
            # Получаем начало и конец рабочего времени
            start_time = datetime.strptime(work_period["start"], "%H:%M").time()
            end_time = datetime.strptime(work_period["end"], "%H:%M").time()
            
            # Генерируем слоты для периода
            period_slots = self._generate_period_slots(
                work_date=work_date,
                start_time=start_time,
                end_time=end_time,
                session_duration_minutes=session_duration_minutes,
                break_between_sessions_minutes=break_between_sessions_minutes,
                break_time=break_time,
                price_per_time=price_per_time,
                party_id=party_id,
                setting_id=setting_id
            )
            daily_slots.extend(period_slots)
        
        return daily_slots

    def _generate_period_slots(
        self,
        work_date: date,
        start_time: time,
        end_time: time,
        session_duration_minutes: int,
        break_between_sessions_minutes: int,
        break_time: List[dict],
        price_per_time: List[dict],
        party_id: int,
        setting_id: int
    ) -> List[dict]:
        """Генерирует слоты для рабочего периода."""
        slots = []
        
        # Преобразуем время перерывов
        breaks = []
        for break_period in break_time:
            break_start = datetime.strptime(break_period["start"], "%H:%M").time()
            break_end = datetime.strptime(break_period["end"], "%H:%M").time()
            breaks.append((break_start, break_end))
        
        # Текущее время для генерации слотов
        current_time = datetime.combine(work_date, start_time)
        end_datetime = datetime.combine(work_date, end_time)
        
        while current_time < end_datetime:
            # Вычисляем время окончания сессии
            session_end = current_time + timedelta(minutes=session_duration_minutes)
            
            # Проверяем, что сессия помещается в рабочее время
            if session_end > end_datetime:
                break
            
            # Проверяем пересечение с перерывами
            slot_start_time = current_time.time()
            slot_end_time = session_end.time()
            
            if not self._is_slot_overlapping_with_breaks(slot_start_time, slot_end_time, breaks):
                # Найдём подходящую цену
                slot_price = self._find_price_for_slot(slot_start_time, slot_end_time, price_per_time)
                
                if slot_price is not None:  # Создаем слот только если найдена цена
                    slot = {
                        "party_id": party_id,
                        "setting_id": setting_id,
                        "day": work_date,  # Передаем объект date
                        "start_at": slot_start_time,  # Передаем объект time
                        "end_at": slot_end_time,  # Передаем объект time
                        "price": slot_price,
                        "is_booked": False,
                        "is_paid": False
                    }
                    slots.append(slot)
            
            # Переходим к следующему слоту
            current_time = session_end + timedelta(minutes=break_between_sessions_minutes)
        
        return slots

    def _is_slot_overlapping_with_breaks(
        self, 
        slot_start: time, 
        slot_end: time, 
        breaks: List[tuple[time, time]]
    ) -> bool:
        """Проверяет, пересекается ли слот с перерывами."""
        for break_start, break_end in breaks:
            # Проверяем пересечение временных интервалов
            if not (slot_end <= break_start or slot_start >= break_end):
                return True  # Есть пересечение
        return False

    def _find_price_for_slot(
        self, 
        slot_start: time, 
        slot_end: time, 
        price_per_time: List[dict]
    ) -> float | None:
        """Находит подходящую цену для слота."""
        for price_period in price_per_time:
            period_start = datetime.strptime(price_period["start"], "%H:%M").time()
            period_end = datetime.strptime(price_period["end"], "%H:%M").time()
            
            # Проверяем, что слот полностью помещается в ценовой период
            if slot_start >= period_start and slot_end <= period_end:
                return float(price_period["price"])
        
        return None  # Подходящая цена не найдена

    async def _save_schedule_records(self, slots: List[dict]) -> List[ScheduleRecordDTO]:
        """Сохраняет сгенерированные слоты в базу данных."""
        saved_records = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for slot_data in slots:
            # Создаем сущность расписания
            schedule_entity = FieldPartyScheduleEntity(
                party_id=slot_data["party_id"],
                setting_id=slot_data["setting_id"],
                day=slot_data["day"],  # Уже объект date
                start_at=slot_data["start_at"],  # Уже объект time
                end_at=slot_data["end_at"],  # Уже объект time
                price=slot_data["price"],
                is_booked=slot_data["is_booked"],
                is_paid=slot_data["is_paid"]
            )
            
            self.db.add(schedule_entity)
            await self.db.flush()  # Получаем ID
            
            # Создаем DTO для ответа
            record_dto = ScheduleRecordDTO(
                party_id=schedule_entity.party_id,
                setting_id=schedule_entity.setting_id,
                day=schedule_entity.day.strftime("%Y-%m-%d"),
                start_at=schedule_entity.start_at.strftime("%H:%M"),
                end_at=schedule_entity.end_at.strftime("%H:%M"),
                price=schedule_entity.price,
                is_booked=schedule_entity.is_booked,
                is_paid=schedule_entity.is_paid,
                created_at=current_time,
                updated_at=current_time,
                deleted_at=None
            )
            saved_records.append(record_dto)
        
        await self.db.commit()
        return saved_records