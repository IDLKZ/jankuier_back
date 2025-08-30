from datetime import datetime, date, time, timedelta
from typing import List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from app.use_case.base_case import BaseUseCase
from app.entities.field_party_schedule_settings_entity import FieldPartyScheduleSettingsEntity
from app.entities.field_party_schedule_entity import FieldPartyScheduleEntity
from app.adapters.repository.base_repository import BaseRepository
from app.adapters.dto.field_party_schedule_settings.schedule_generator_dto import (
    ScheduleGeneratorResponseDTO,
    ScheduleRecordDTO
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.redis_client import redis_client


class PreviewFieldPartyScheduleCase(BaseUseCase[ScheduleGeneratorResponseDTO]):
    """UseCase для виртуальной генерации (предварительного просмотра) расписания поля на указанную дату."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings_repository = BaseRepository(FieldPartyScheduleSettingsEntity, db)
        self.schedule_repository = BaseRepository(FieldPartyScheduleEntity, db)

    async def execute(self, field_party_id: int, day: str) -> ScheduleGeneratorResponseDTO:
        """
        Генерирует виртуальное расписание для поля на указанную дату с Redis кэшированием.
        
        Args:
            field_party_id: ID партии поля
            day: Дата для генерации в формате "YYYY-MM-DD"
        """
        await self.validate(field_party_id=field_party_id, day=day)
        
        # Парсим дату
        target_date = datetime.strptime(day, "%Y-%m-%d").date()
        
        # Получаем настройки расписания
        settings = await self._get_settings_for_party(field_party_id)
        if not settings:
            return ScheduleGeneratorResponseDTO(
                success=False,
                message="Настройки расписания для данной партии поля не найдены",
                generated_count=0,
                schedule_records=[]
            )
        
        # Проверяем, что дата попадает в активный период
        if not (settings.active_start_at <= target_date <= settings.active_end_at):
            return ScheduleGeneratorResponseDTO(
                success=False,
                message=f"Дата {day} не попадает в активный период расписания ({settings.active_start_at} - {settings.active_end_at})",
                generated_count=0,
                schedule_records=[]
            )
        
        # Проверяем, что это рабочий день
        weekday = target_date.isoweekday()  # 1=понедельник, 7=воскресенье
        if weekday not in settings.working_days:
            return ScheduleGeneratorResponseDTO(
                success=False,
                message=f"Дата {day} не является рабочим днем согласно настройкам",
                generated_count=0,
                schedule_records=[]
            )
        
        # Проверяем, что дата не в исключенных
        if settings.excluded_dates and target_date in settings.excluded_dates:
            return ScheduleGeneratorResponseDTO(
                success=False,
                message=f"Дата {day} исключена из расписания",
                generated_count=0,
                schedule_records=[]
            )
        
        # Пытаемся получить данные из Redis кэша
        cache_key = f"schedule:preview:{field_party_id}:{day}"
        cached_data = await self._get_cached_schedule(cache_key, settings.updated_at)
        
        if cached_data:
            # Даже если данные из кэша, нужно синхронизировать статус бронирования
            # так как бронирования могут изменяться чаще настроек
            updated_records = await self._sync_cached_booking_status(cached_data.schedule_records, target_date)
            cached_data.schedule_records = updated_records
            return cached_data
        
        # Генерируем слоты для указанной даты
        generated_slots = await self._generate_schedule_slots_for_date(settings, target_date)
        
        # Синхронизируем статус бронирования с реальными записями из БД
        synced_slots = await self._sync_booking_status(generated_slots, target_date)
        
        # Конвертируем слоты в ScheduleRecordDTO
        schedule_records = self._convert_slots_to_dto(synced_slots)
        
        # Создаем ответ
        response = ScheduleGeneratorResponseDTO(
            success=True,
            message=f"Сгенерировано {len(schedule_records)} слотов расписания для {day}",
            generated_count=len(schedule_records),
            schedule_records=schedule_records
        )
        
        # Сохраняем в кэш
        await self._cache_schedule(cache_key, response, settings.updated_at)
        
        return response

    async def validate(self, field_party_id: int, day: str) -> None:
        """Валидация входных параметров."""
        if field_party_id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID партии поля должен быть больше нуля"
            )
        
        # Проверяем формат даты
        try:
            datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            raise AppExceptionResponse.bad_request(
                message="Неверный формат даты. Используйте YYYY-MM-DD"
            )

    async def _get_settings_for_party(self, field_party_id: int) -> FieldPartyScheduleSettingsEntity | None:
        """Получает активные настройки расписания для партии поля."""
        filters = [
            FieldPartyScheduleSettingsEntity.party_id == field_party_id,
            FieldPartyScheduleSettingsEntity.deleted_at.is_(None)
        ]
        results = await self.settings_repository.get_all(filters=filters)
        return results[0] if results else None

    async def _generate_schedule_slots_for_date(self, settings: FieldPartyScheduleSettingsEntity, target_date: date) -> List[dict]:
        """Генерирует слоты расписания для указанной даты."""
        slots = []
        
        # Генерируем слоты для указанной даты
        daily_slots = self._generate_daily_slots(
            work_date=target_date,
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
        
        # Получаем день недели (1=понедельник, 7=воскресенье)
        weekday = work_date.isoweekday()
        
        # Фильтруем рабочие периоды по дню недели
        day_working_time = [
            period for period in working_time 
            if period.get("day") == weekday
        ]
        
        # Фильтруем перерывы по дню недели
        day_break_time = [
            brk for brk in break_time 
            if brk.get("day") == weekday
        ]
        
        # Фильтруем цены по дню недели
        day_price_per_time = [
            price for price in price_per_time 
            if price.get("day") == weekday
        ]
        
        for work_period in day_working_time:
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
                break_time=day_break_time,
                price_per_time=day_price_per_time,
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
            
            # Проверяем, находится ли текущий слот в перерыве
            overlapping_break = self._find_overlapping_break(slot_start_time, slot_end_time, breaks)
            
            if overlapping_break is None:
                # Слот не пересекается с перерывом - создаем его
                slot_price = self._find_price_for_slot(slot_start_time, slot_end_time, price_per_time)
                
                if slot_price is not None:  # Создаем слот только если найдена цена
                    slot = {
                        "party_id": party_id,
                        "setting_id": setting_id,
                        "day": work_date,
                        "start_at": slot_start_time,
                        "end_at": slot_end_time,
                        "price": slot_price,
                        "is_booked": False,
                        "is_paid": False
                    }
                    slots.append(slot)
                
                # Переходим к следующему слоту
                current_time = session_end + timedelta(minutes=break_between_sessions_minutes)
            else:
                # Слот пересекается с перерывом - пропускаем время до конца перерыва
                break_start, break_end = overlapping_break
                # Возобновляем расписание с времени окончания перерыва (end)
                current_time = datetime.combine(work_date, break_end)
        
        return slots

    def _find_overlapping_break(
        self, 
        slot_start: time, 
        slot_end: time, 
        breaks: List[tuple[time, time]]
    ) -> tuple[time, time] | None:
        """Находит перерыв, который пересекается со слотом. Возвращает tuple (break_start, break_end) или None."""
        for break_start, break_end in breaks:
            # Проверяем пересечение временных интервалов
            if not (slot_end <= break_start or slot_start >= break_end):
                return (break_start, break_end)  # Возвращаем пересекающийся перерыв
        return None

    def _is_slot_overlapping_with_breaks(
        self, 
        slot_start: time, 
        slot_end: time, 
        breaks: List[tuple[time, time]]
    ) -> bool:
        """Проверяет, пересекается ли слот с перерывами."""
        return self._find_overlapping_break(slot_start, slot_end, breaks) is not None

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

    def _convert_slots_to_dto(self, slots: List[dict]) -> List[ScheduleRecordDTO]:
        """Конвертирует слоты в ScheduleRecordDTO без сохранения в БД."""
        schedule_records = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for slot_data in slots:
            record_dto = ScheduleRecordDTO(
                party_id=slot_data["party_id"],
                setting_id=slot_data["setting_id"],
                day=slot_data["day"].strftime("%Y-%m-%d"),
                start_at=slot_data["start_at"].strftime("%H:%M"),
                end_at=slot_data["end_at"].strftime("%H:%M"),
                price=slot_data["price"],
                is_booked=slot_data["is_booked"],
                is_paid=slot_data["is_paid"],
                created_at=current_time,
                updated_at=current_time,
                deleted_at=None
            )
            schedule_records.append(record_dto)
        
        return schedule_records

    async def _get_cached_schedule(self, cache_key: str, settings_updated_at: datetime) -> ScheduleGeneratorResponseDTO | None:
        """Получает данные из Redis кэша с проверкой актуальности."""
        try:
            cached_raw = redis_client.get(cache_key)
            if not cached_raw:
                return None
            
            cached_data = json.loads(cached_raw)
            
            # Проверяем актуальность кэша по updated_at
            cached_updated_at = datetime.fromisoformat(cached_data["settings_updated_at"])
            if cached_updated_at != settings_updated_at:
                # Кэш устарел, удаляем его
                redis_client.delete(cache_key)
                return None
            
            # Восстанавливаем объект ScheduleGeneratorResponseDTO
            schedule_records = [
                ScheduleRecordDTO(**record) for record in cached_data["schedule_records"]
            ]
            
            return ScheduleGeneratorResponseDTO(
                success=cached_data["success"],
                message=cached_data["message"],
                generated_count=cached_data["generated_count"],
                schedule_records=schedule_records
            )
        except Exception:
            # В случае ошибки парсинга удаляем неверный кэш
            redis_client.delete(cache_key)
            return None

    async def _cache_schedule(
        self, 
        cache_key: str, 
        response: ScheduleGeneratorResponseDTO, 
        settings_updated_at: datetime
    ) -> None:
        """Сохраняет расписание в Redis кэш."""
        try:
            # Конвертируем ScheduleRecordDTO в словари для JSON
            records_data = []
            for record in response.schedule_records:
                records_data.append({
                    "party_id": record.party_id,
                    "setting_id": record.setting_id,
                    "day": record.day,
                    "start_at": record.start_at,
                    "end_at": record.end_at,
                    "price": record.price,
                    "is_booked": record.is_booked,
                    "is_paid": record.is_paid,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at,
                    "deleted_at": record.deleted_at
                })
            
            cache_data = {
                "success": response.success,
                "message": response.message,
                "generated_count": response.generated_count,
                "schedule_records": records_data,
                "settings_updated_at": settings_updated_at.isoformat()
            }
            
            # Кэшируем на 24 часа (86400 секунд)
            redis_client.setex(cache_key, 86400, json.dumps(cache_data, default=str))
        except Exception:
            # Если не удалось закэшировать, продолжаем работу без кэша
            pass

    async def _sync_booking_status(self, generated_slots: List[dict], target_date: date) -> List[dict]:
        """Синхронизирует статус бронирования с реальными записями FieldSchedule."""
        try:
            # Получаем все забронированные слоты из базы на указанную дату
            filters = [
                FieldPartyScheduleEntity.day == target_date,
                FieldPartyScheduleEntity.is_booked == True,
                FieldPartyScheduleEntity.deleted_at.is_(None)
            ]
            
            booked_schedules = await self.schedule_repository.get_all(filters=filters)
            
            # Создаем словарь для быстрого поиска забронированных слотов
            booked_slots = {}
            for schedule in booked_schedules:
                key = f"{schedule.party_id}:{schedule.start_at.strftime('%H:%M')}:{schedule.end_at.strftime('%H:%M')}"
                booked_slots[key] = {
                    'is_booked': schedule.is_booked,
                    'is_paid': schedule.is_paid
                }
            
            # Обновляем статус бронирования в сгенерированных слотах
            for slot in generated_slots:
                start_time_str = slot['start_at'].strftime('%H:%M') if hasattr(slot['start_at'], 'strftime') else str(slot['start_at'])
                end_time_str = slot['end_at'].strftime('%H:%M') if hasattr(slot['end_at'], 'strftime') else str(slot['end_at'])
                slot_key = f"{slot['party_id']}:{start_time_str}:{end_time_str}"
                if slot_key in booked_slots:
                    slot['is_booked'] = True
                    slot['is_paid'] = booked_slots[slot_key].get('is_paid', False)
            
            return generated_slots
        except Exception:
            # В случае ошибки возвращаем исходные данные
            return generated_slots

    async def _sync_cached_booking_status(self, cached_records: List[ScheduleRecordDTO], target_date: date) -> List[ScheduleRecordDTO]:
        """Синхронизирует статус бронирования для записей из кэша."""
        try:
            # Получаем все забронированные слоты из базы на указанную дату
            filters = [
                FieldPartyScheduleEntity.day == target_date,
                FieldPartyScheduleEntity.is_booked == True,
                FieldPartyScheduleEntity.deleted_at.is_(None)
            ]
            
            booked_schedules = await self.schedule_repository.get_all(filters=filters)
            
            # Создаем словарь для быстрого поиска забронированных слотов
            booked_slots = {}
            for schedule in booked_schedules:
                key = f"{schedule.party_id}:{schedule.start_at.strftime('%H:%M')}:{schedule.end_at.strftime('%H:%M')}"
                booked_slots[key] = {
                    'is_booked': schedule.is_booked,
                    'is_paid': schedule.is_paid
                }
            
            # Обновляем статус бронирования в кэшированных записях
            for record in cached_records:
                record_key = f"{record.party_id}:{record.start_at}:{record.end_at}"
                if record_key in booked_slots:
                    record.is_booked = booked_slots[record_key]['is_booked']
                    record.is_paid = booked_slots[record_key]['is_paid']
                else:
                    # Если слот не найден в базе, он свободен
                    record.is_booked = False
                    record.is_paid = False
            
            return cached_records
        except Exception:
            # В случае ошибки возвращаем исходные данные
            return cached_records