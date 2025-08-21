from pydantic import BaseModel
from app.adapters.dto.field_party.field_party_dto import FieldPartyRDTO
from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
    FieldPartyScheduleSettingsRDTO,
)
from app.shared.dto_constants import DTOConstant


class FieldPartyScheduleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FieldPartyScheduleCDTO(BaseModel):
    party_id: DTOConstant.StandardUnsignedIntegerField(description="ID площадки")
    setting_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID настроек расписания"
    )
    day: DTOConstant.StandardDateField(description="Дата")
    start_at: DTOConstant.StandardTimeField(description="Время начала")
    end_at: DTOConstant.StandardTimeField(description="Время окончания")
    price: DTOConstant.StandardPriceField(description="Цена за период")
    is_booked: DTOConstant.StandardBooleanFalseField(description="Забронировано")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачено")

    class Config:
        from_attributes = True


class FieldPartyScheduleRDTO(FieldPartyScheduleDTO):
    party_id: DTOConstant.StandardUnsignedIntegerField(description="ID площадки")
    setting_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID настроек расписания"
    )
    day: DTOConstant.StandardDateField(description="Дата")
    start_at: DTOConstant.StandardTimeField(description="Время начала")
    end_at: DTOConstant.StandardTimeField(description="Время окончания")
    price: DTOConstant.StandardPriceField(description="Цена за период")
    is_booked: DTOConstant.StandardBooleanFalseField(description="Забронировано")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачено")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class FieldPartyScheduleWithRelationsRDTO(FieldPartyScheduleRDTO):
    party: FieldPartyRDTO | None = None
    setting: FieldPartyScheduleSettingsRDTO | None = None

    class Config:
        from_attributes = True


class FieldPartyScheduleUpdateDTO(BaseModel):
    """DTO для обновления расписания площадки - все поля опциональные"""

    day: DTOConstant.StandardDateField(description="Дата") | None = None
    start_at: DTOConstant.StandardTimeField(description="Время начала") | None = None
    end_at: DTOConstant.StandardTimeField(description="Время окончания") | None = None
    price: DTOConstant.StandardPriceField(description="Цена за период") | None = None
    is_booked: (
        DTOConstant.StandardBooleanFalseField(description="Забронировано") | None
    ) = None
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачено") | None = None

    class Config:
        from_attributes = True


class FieldPartyScheduleBulkCDTO(BaseModel):
    """DTO для массового создания расписаний площадки"""

    party_id: DTOConstant.StandardUnsignedIntegerField(description="ID площадки")
    setting_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID настроек расписания"
    )
    schedules: list[dict] = (
        []
    )  # [{"day": "2025-01-01", "start_at": "09:00", "end_at": "10:00", "price": 15000}]

    class Config:
        from_attributes = True
