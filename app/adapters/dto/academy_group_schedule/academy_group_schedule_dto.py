from pydantic import BaseModel
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.shared.dto_constants import DTOConstant


class AcademyGroupScheduleDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyGroupScheduleCDTO(BaseModel):
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    training_date: DTOConstant.StandardDateField(description="Дата тренировки")
    start_at: DTOConstant.StandardTimeField(description="Время начала")
    end_at: DTOConstant.StandardTimeField(description="Время окончания")
    reschedule_start_at: DTOConstant.StandardNullableDateTimeField(description="Новое время начала при переносе")
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(description="Новое время окончания при переносе")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности расписания")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Тренировка отменена")
    is_finished: DTOConstant.StandardBooleanFalseField(description="Тренировка завершена")

    class Config:
        from_attributes = True


class AcademyGroupScheduleRDTO(AcademyGroupScheduleDTO):
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    training_date: DTOConstant.StandardDateField(description="Дата тренировки")
    start_at: DTOConstant.StandardTimeField(description="Время начала")
    end_at: DTOConstant.StandardTimeField(description="Время окончания")
    reschedule_start_at: DTOConstant.StandardNullableDateTimeField(description="Новое время начала при переносе")
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(description="Новое время окончания при переносе")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности расписания")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Тренировка отменена")
    is_finished: DTOConstant.StandardBooleanFalseField(description="Тренировка завершена")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class AcademyGroupScheduleWithRelationsRDTO(AcademyGroupScheduleRDTO):
    group: AcademyGroupRDTO | None = None

    class Config:
        from_attributes = True


class AcademyGroupScheduleUpdateDTO(BaseModel):
    """DTO для обновления расписания группы - все поля опциональные"""
    training_date: DTOConstant.StandardDateField(description="Дата тренировки") | None = None
    start_at: DTOConstant.StandardTimeField(description="Время начала") | None = None
    end_at: DTOConstant.StandardTimeField(description="Время окончания") | None = None
    reschedule_start_at: DTOConstant.StandardNullableDateTimeField(description="Новое время начала при переносе") | None = None
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(description="Новое время окончания при переносе") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности расписания") | None = None
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Тренировка отменена") | None = None
    is_finished: DTOConstant.StandardBooleanFalseField(description="Тренировка завершена") | None = None

    class Config:
        from_attributes = True


class AcademyGroupScheduleBulkCDTO(BaseModel):
    """DTO для массового создания расписаний группы"""
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    schedules: list[dict] = []  # [{"training_date": "2025-01-01", "start_at": "09:00", "end_at": "10:00"}]

    class Config:
        from_attributes = True