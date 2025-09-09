from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery
from app.adapters.filters.base_filter import BaseFilter
from app.entities import TicketonOrderEntity
from app.shared.query_constants import AppQueryConstants


class TicketonOrderFilter(BaseFilter[TicketonOrderEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по шоу, email, телефону, причине отмены"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        user_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по пользователям"
        ),
        status_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по статусам заказа"
        ),
        payment_transaction_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по транзакциям"
        ),
        lang: str | None = AppQueryConstants.StandardOptionalStringQuery(
            "Фильтрация по языку"
        ),
        currency: str | None = AppQueryConstants.StandardOptionalStringQuery(
            "Фильтрация по валюте"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности заказа"
        ),
        is_paid: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу оплаты"
        ),
        is_canceled: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу отмены"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=TicketonOrderEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.user_ids = user_ids
        self.status_ids = status_ids
        self.payment_transaction_ids = payment_transaction_ids
        self.lang = lang
        self.currency = currency
        self.is_active = is_active
        self.is_paid = is_paid
        self.is_canceled = is_canceled
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["show", "pre_sale", "sale", "reservation_id", "email", "phone", "cancel_reason", "status"]

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

        if self.user_ids:
            filters.append(self.model.user_id.in_(self.user_ids))

        if self.status_ids:
            filters.append(self.model.status_id.in_(self.status_ids))

        if self.payment_transaction_ids:
            filters.append(self.model.payment_transaction_id.in_(self.payment_transaction_ids))

        if self.lang:
            filters.append(self.model.lang.ilike(f"%{self.lang}%"))

        if self.currency:
            filters.append(self.model.currency.ilike(f"%{self.currency}%"))

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_paid is not None:
            filters.append(self.model.is_paid.is_(self.is_paid))

        if self.is_canceled is not None:
            filters.append(self.model.is_canceled.is_(self.is_canceled))

        return filters