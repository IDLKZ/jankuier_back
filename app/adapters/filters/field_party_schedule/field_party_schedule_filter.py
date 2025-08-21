from datetime import date, time
from decimal import Decimal
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import FieldPartyScheduleEntity
from app.shared.query_constants import AppQueryConstants


class FieldPartyScheduleFilter(BaseFilter[FieldPartyScheduleEntity]):
    def __init__(
        self,
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
        setting_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по настройкам расписания"
        ),
        day_from: date | None = AppQueryConstants.StandardOptionalDateQuery("Дата от"),
        day_to: date | None = AppQueryConstants.StandardOptionalDateQuery("Дата до"),
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        is_booked: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация забронированных слотов"
        ),
        is_paid: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация оплаченных слотов"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=FieldPartyScheduleEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
        )
        self.party_ids = party_ids
        self.setting_ids = setting_ids
        self.day_from = day_from
        self.day_to = day_to
        self.min_price = min_price
        self.max_price = max_price
        self.is_booked = is_booked
        self.is_paid = is_paid
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.party_ids:
            filters.append(FieldPartyScheduleEntity.party_id.in_(self.party_ids))

        if self.setting_ids:
            filters.append(FieldPartyScheduleEntity.setting_id.in_(self.setting_ids))

        if self.day_from is not None:
            filters.append(FieldPartyScheduleEntity.day >= self.day_from)

        if self.day_to is not None:
            filters.append(FieldPartyScheduleEntity.day <= self.day_to)

        if self.min_price is not None:
            filters.append(FieldPartyScheduleEntity.price >= self.min_price)

        if self.max_price is not None:
            filters.append(FieldPartyScheduleEntity.price <= self.max_price)

        if self.is_booked is not None:
            filters.append(self.model.is_booked.is_(self.is_booked))

        if self.is_paid is not None:
            filters.append(self.model.is_paid.is_(self.is_paid))

        return filters
