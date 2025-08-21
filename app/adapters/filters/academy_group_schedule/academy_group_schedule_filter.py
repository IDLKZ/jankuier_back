from datetime import date, time, datetime
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import AcademyGroupScheduleEntity
from app.shared.query_constants import AppQueryConstants


class AcademyGroupScheduleFilter(BaseFilter[AcademyGroupScheduleEntity]):
    def __init__(
        self,
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        group_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по группам академий"
        ),
        training_date_from: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Дата тренировки от"
        ),
        training_date_to: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Дата тренировки до"
        ),
        start_time_from: time | None = AppQueryConstants.StandardOptionalTimeQuery(
            "Время начала от"
        ),
        start_time_to: time | None = AppQueryConstants.StandardOptionalTimeQuery(
            "Время начала до"
        ),
        end_time_from: time | None = AppQueryConstants.StandardOptionalTimeQuery(
            "Время окончания от"
        ),
        end_time_to: time | None = AppQueryConstants.StandardOptionalTimeQuery(
            "Время окончания до"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу активности"
        ),
        is_canceled: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу отмены"
        ),
        is_finished: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу завершения"
        ),
        has_reschedule: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по наличию переноса"
        ),
        reschedule_start_from: (
            datetime | None
        ) = AppQueryConstants.StandardOptionalDateTimeQuery("Перенос начала от"),
        reschedule_start_to: (
            datetime | None
        ) = AppQueryConstants.StandardOptionalDateTimeQuery("Перенос начала до"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=AcademyGroupScheduleEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
        )
        self.group_ids = group_ids
        self.training_date_from = training_date_from
        self.training_date_to = training_date_to
        self.start_time_from = start_time_from
        self.start_time_to = start_time_to
        self.end_time_from = end_time_from
        self.end_time_to = end_time_to
        self.is_active = is_active
        self.is_canceled = is_canceled
        self.is_finished = is_finished
        self.has_reschedule = has_reschedule
        self.reschedule_start_from = reschedule_start_from
        self.reschedule_start_to = reschedule_start_to
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.group_ids:
            filters.append(AcademyGroupScheduleEntity.group_id.in_(self.group_ids))

        if self.training_date_from:
            filters.append(
                AcademyGroupScheduleEntity.training_date >= self.training_date_from
            )

        if self.training_date_to:
            filters.append(
                AcademyGroupScheduleEntity.training_date <= self.training_date_to
            )

        if self.start_time_from:
            filters.append(AcademyGroupScheduleEntity.start_at >= self.start_time_from)

        if self.start_time_to:
            filters.append(AcademyGroupScheduleEntity.start_at <= self.start_time_to)

        if self.end_time_from:
            filters.append(AcademyGroupScheduleEntity.end_at >= self.end_time_from)

        if self.end_time_to:
            filters.append(AcademyGroupScheduleEntity.end_at <= self.end_time_to)

        if self.is_active is not None:
            filters.append(AcademyGroupScheduleEntity.is_active == self.is_active)

        if self.is_canceled is not None:
            filters.append(AcademyGroupScheduleEntity.is_canceled == self.is_canceled)

        if self.is_finished is not None:
            filters.append(AcademyGroupScheduleEntity.is_finished == self.is_finished)

        if self.has_reschedule is not None:
            if self.has_reschedule:
                filters.append(
                    AcademyGroupScheduleEntity.reschedule_start_at.is_not(None)
                )
            else:
                filters.append(AcademyGroupScheduleEntity.reschedule_start_at.is_(None))

        if self.reschedule_start_from:
            filters.append(
                AcademyGroupScheduleEntity.reschedule_start_at
                >= self.reschedule_start_from
            )

        if self.reschedule_start_to:
            filters.append(
                AcademyGroupScheduleEntity.reschedule_start_at
                <= self.reschedule_start_to
            )

        return filters
