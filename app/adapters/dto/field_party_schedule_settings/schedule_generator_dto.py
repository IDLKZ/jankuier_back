from datetime import date
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

from app.shared.dto_constants import DTOConstant


class WorkingTimeDTO(BaseModel):
    """DTO для рабочего времени"""
    start: str = Field(..., description="Время начала в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    end: str = Field(..., description="Время окончания в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")


class BreakTimeDTO(BaseModel):
    """DTO для времени перерыва"""
    start: str = Field(..., description="Время начала перерыва в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    end: str = Field(..., description="Время окончания перерыва в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")


class PricePerTimeDTO(BaseModel):
    """DTO для ценообразования по времени"""
    start: str = Field(..., description="Время начала ценового диапазона в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    end: str = Field(..., description="Время окончания ценового диапазона в формате HH:MM", pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    price: float = Field(..., description="Цена за сессию в данном временном диапазоне", gt=0)


class PartyDTO(BaseModel):
    """DTO для информации о площадке"""
    id: int = Field(..., description="ID площадки", gt=0)


class ScheduleSettingsItemDTO(BaseModel):
    """DTO для одной записи настроек расписания"""
    id: int = Field(..., description="ID настройки", gt=0)
    active_start_at: date = Field(..., description="Дата начала активности")
    active_end_at: date = Field(..., description="Дата окончания активности")
    working_days: List[int] = Field(..., description="Рабочие дни недели [1-7]", min_items=1, max_items=7)
    excluded_dates: Optional[List[str]] = Field(None, description="Исключенные даты в формате YYYY-MM-DD")
    working_time: List[WorkingTimeDTO] = Field(..., description="Рабочее время", min_items=1)
    break_time: List[BreakTimeDTO] = Field(default_factory=list, description="Время перерывов")
    price_per_time: List[PricePerTimeDTO] = Field(..., description="Ценообразование по времени", min_items=1)
    session_minute_int: int = Field(..., description="Длительность сессии в минутах", gt=0)
    break_between_session_int: int = Field(..., description="Перерыв между сессиями в минутах", ge=0)
    booked_limit: int = Field(..., description="Лимит бронирований", gt=0)

    @validator('working_days')
    def validate_working_days(cls, v):
        """Валидация рабочих дней недели"""
        for day in v:
            if day < 1 or day > 7:
                raise ValueError('Рабочие дни должны быть в диапазоне 1-7 (1=понедельник, 7=воскресенье)')
        return v

    @validator('excluded_dates')
    def validate_excluded_dates(cls, v):
        """Валидация формата исключенных дат"""
        if v:
            from datetime import datetime
            for date_str in v:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f'Неверный формат даты: {date_str}. Используйте YYYY-MM-DD')
        return v

    @validator('active_end_at')
    def validate_date_range(cls, v, values):
        """Валидация диапазона дат"""
        if 'active_start_at' in values and v < values['active_start_at']:
            raise ValueError('Дата окончания должна быть больше или равна дате начала')
        return v


class ScheduleGeneratorInputDTO(BaseModel):
    """DTO для входных данных генератора расписания"""
    items: List[ScheduleSettingsItemDTO] = Field(..., description="Список настроек расписания", min_items=1)
    party: PartyDTO = Field(..., description="Информация о площадке")


class ScheduleGeneratorRequestDTO(BaseModel):
    """DTO для запроса генерации расписания"""
    field_party_id: int = Field(..., description="ID площадки", gt=0)
    day: str = Field(..., description="Дата для генерации в формате YYYY-MM-DD", pattern=r"^\d{4}-\d{2}-\d{2}$")
    delete_existing: bool = Field(True, description="Удалить существующие записи на эту дату")
    schedule_data: ScheduleGeneratorInputDTO = Field(..., description="Данные настроек расписания")

    @validator('day')
    def validate_day_format(cls, v):
        """Валидация формата даты"""
        from datetime import datetime
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Неверный формат даты. Используйте YYYY-MM-DD')
        return v


class ScheduleRecordDTO(BaseModel):
    """DTO для одной записи расписания"""
    party_id: int
    setting_id: int
    day: str
    start_at: str
    end_at: str
    price: float
    is_booked: bool
    is_paid: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str]


class ScheduleGeneratorResponseDTO(BaseModel):
    """DTO для ответа генератора расписания"""
    success: bool = Field(..., description="Статус операции")
    message: str = Field(..., description="Сообщение о результате")
    generated_count: int = Field(..., description="Количество сгенерированных записей")
    schedule_records: List[ScheduleRecordDTO] = Field(default_factory=list, description="Сгенерированные записи расписания")