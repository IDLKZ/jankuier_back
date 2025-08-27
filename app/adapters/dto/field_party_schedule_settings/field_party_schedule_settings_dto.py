from pydantic import BaseModel
from app.adapters.dto.field_party.field_party_dto import FieldPartyRDTO
from app.shared.dto_constants import DTOConstant


class FieldPartyScheduleSettingsDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FieldPartyScheduleSettingsCDTO(BaseModel):
    party_id: DTOConstant.StandardUnsignedIntegerField(description="ID площадки")
    active_start_at: DTOConstant.StandardDateField(description="Дата начала активности")
    active_end_at: DTOConstant.StandardDateField(
        description="Дата окончания активности"
    )
    working_days: DTOConstant.StandardArrayIntegerField(
        description="Рабочие дни [1,2,3,4,5]"
    )
    excluded_dates: DTOConstant.StandardNullableArrayDateField(
        description="Исключенные даты [гггг-мм-дд]"
    )
    working_time: DTOConstant.StandardScheduleTimeField(
        description="Рабочее время в формате JSON 1:[{start_at:09:00, end_at:00:00}]"
    )
    break_time: DTOConstant.StandardScheduleTimeField(
        description="Время перерыва в формате JSON 1:[09:00 - 16:00]"
    )
    price_per_time: DTOConstant.StandardPricePerTimeField(
        description="Цены по времени в формате JSON 1:[{start_at:09:00, end_at: 18:00, price: 16 000.00, start_at:18:00, end_at:00:00, price:20 000. 00}"
    )
    session_minute_int: DTOConstant.StandardIntegerField(
        description="Длительность сессии в минутах"
    )
    break_between_session_int: DTOConstant.StandardIntegerField(
        description="Перерыв между сессиями в минутах"
    )
    booked_limit: DTOConstant.StandardIntegerField(description="Лимит бронирований")

    class Config:
        from_attributes = True


class FieldPartyScheduleSettingsRDTO(FieldPartyScheduleSettingsDTO):
    party_id: DTOConstant.StandardUnsignedIntegerField(description="ID площадки")
    active_start_at: DTOConstant.StandardDateField(description="Дата начала активности")
    active_end_at: DTOConstant.StandardDateField(
        description="Дата окончания активности"
    )
    working_days: DTOConstant.StandardArrayIntegerField(
        description="Рабочие дни [1,2,3,4,5]"
    )
    excluded_dates: DTOConstant.StandardNullableArrayDateField(
        description="Исключенные даты [гггг-мм-дд]"
    )
    working_time: DTOConstant.StandardScheduleTimeField(
        description="Рабочее время в формате JSON"
    )
    break_time: DTOConstant.StandardScheduleTimeField(
        description="Время перерыва в формате JSON"
    )
    price_per_time: DTOConstant.StandardPricePerTimeField(
        description="Цены по времени в формате JSON"
    )
    session_minute_int: DTOConstant.StandardIntegerField(
        description="Длительность сессии в минутах"
    )
    break_between_session_int: DTOConstant.StandardIntegerField(
        description="Перерыв между сессиями в минутах"
    )
    booked_limit: DTOConstant.StandardIntegerField(description="Лимит бронирований")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class FieldPartyScheduleSettingsWithRelationsRDTO(FieldPartyScheduleSettingsRDTO):
    party: FieldPartyRDTO | None = None

    class Config:
        from_attributes = True


class FieldPartyScheduleSettingsUpdateDTO(BaseModel):
    """DTO для обновления настроек расписания площадки - все поля опциональные"""

    active_start_at: (
        DTOConstant.StandardDateField(description="Дата начала активности") | None
    ) = None
    active_end_at: (
        DTOConstant.StandardDateField(description="Дата окончания активности") | None
    ) = None
    working_days: (
        DTOConstant.StandardArrayIntegerField(description="Рабочие дни [1,2,3,4,5]")
        | None
    ) = None
    excluded_dates: (
        DTOConstant.StandardNullableVarcharField(
            description="Исключенные даты в формате JSON"
        )
        | None
    ) = None
    working_time: (
        DTOConstant.StandardScheduleTimeField(description="Рабочее время в формате JSON") | None
    ) = None
    break_time: (
        DTOConstant.StandardScheduleTimeField(description="Время перерыва в формате JSON")
        | None
    ) = None
    price_per_time: (
        DTOConstant.StandardPricePerTimeField(description="Цены по времени в формате JSON")
        | None
    ) = None
    session_minute_int: (
        DTOConstant.StandardIntegerField(description="Длительность сессии в минутах")
        | None
    ) = None
    break_between_session_int: (
        DTOConstant.StandardIntegerField(description="Перерыв между сессиями в минутах")
        | None
    ) = None
    booked_limit: (
        DTOConstant.StandardIntegerField(description="Лимит бронирований") | None
    ) = None

    class Config:
        from_attributes = True
