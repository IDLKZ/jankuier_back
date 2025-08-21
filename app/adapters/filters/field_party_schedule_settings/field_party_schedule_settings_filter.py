from datetime import date
from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import FieldPartyScheduleSettingsEntity
from app.shared.query_constants import AppQueryConstants


class FieldPartyScheduleSettingsFilter(BaseFilter[FieldPartyScheduleSettingsEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по исключенным датам"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        party_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по площадкам"
        ),
        active_start_from: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Начало активности от"
        ),
        active_start_to: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Начало активности до"
        ),
        active_end_from: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Окончание активности от"
        ),
        active_end_to: date | None = AppQueryConstants.StandardOptionalDateQuery(
            "Окончание активности до"
        ),
        min_session_minute: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальная длительность сессии в минутах"
        ),
        max_session_minute: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальная длительность сессии в минутах"
        ),
        min_break_between_session: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальный перерыв между сессиями в минутах"
        ),
        max_break_between_session: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальный перерыв между сессиями в минутах"
        ),
        min_booked_limit: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальный лимит бронирований"
        ),
        max_booked_limit: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальный лимит бронирований"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FieldPartyScheduleSettingsEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.party_ids = party_ids
        self.active_start_from = active_start_from
        self.active_start_to = active_start_to
        self.active_end_from = active_end_from
        self.active_end_to = active_end_to
        self.min_session_minute = min_session_minute
        self.max_session_minute = max_session_minute
        self.min_break_between_session = min_break_between_session
        self.max_break_between_session = max_break_between_session
        self.min_booked_limit = min_booked_limit
        self.max_booked_limit = max_booked_limit
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["excluded_dates"]  # Only string field in the entity

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.search:
            model_columns = {column.key for column in inspect(self.model).columns}
            valid_fields = [
                field for field in self.get_search_filters() if field in model_columns
            ]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).ilike(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )

        if self.party_ids:
            filters.append(
                FieldPartyScheduleSettingsEntity.party_id.in_(self.party_ids)
            )

        if self.active_start_from is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.active_start_at
                >= self.active_start_from
            )

        if self.active_start_to is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.active_start_at <= self.active_start_to
            )

        if self.active_end_from is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.active_end_at >= self.active_end_from
            )

        if self.active_end_to is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.active_end_at <= self.active_end_to
            )

        if self.min_session_minute is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.session_minute_int
                >= self.min_session_minute
            )

        if self.max_session_minute is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.session_minute_int
                <= self.max_session_minute
            )

        if self.min_break_between_session is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.break_between_session_int
                >= self.min_break_between_session
            )

        if self.max_break_between_session is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.break_between_session_int
                <= self.max_break_between_session
            )

        if self.min_booked_limit is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.booked_limit >= self.min_booked_limit
            )

        if self.max_booked_limit is not None:
            filters.append(
                FieldPartyScheduleSettingsEntity.booked_limit <= self.max_booked_limit
            )

        return filters
