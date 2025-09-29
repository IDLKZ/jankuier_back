from datetime import datetime
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import ProductOrderEntity
from app.shared.query_constants import AppQueryConstants


class ProductOrderFilter(BaseFilter[ProductOrderEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по email, телефону, причине отмены"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        user_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по пользователям"
        ),
        status_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по статусам заказа"
        ),
        total_price_from: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Общая стоимость заказа от"
        ),
        total_price_to: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Общая стоимость заказа до"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активным заказам"
        ),
        is_canceled: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по отмененным заказам"
        ),
        is_paid: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по оплаченным заказам"
        ),
        is_refunded: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по возвращенным заказам"
        ),
        paid_from: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата оплаты от"
        ),
        paid_to: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата оплаты до"
        ),
        created_from: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата создания от"
        ),
        created_to: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата создания до"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductOrderEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.user_ids = user_ids
        self.status_ids = status_ids
        self.total_price_from = total_price_from
        self.total_price_to = total_price_to
        self.is_active = is_active
        self.is_canceled = is_canceled
        self.is_paid = is_paid
        self.is_refunded = is_refunded
        self.paid_from = paid_from
        self.paid_to = paid_to
        self.created_from = created_from
        self.created_to = created_to
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        """Поля для текстового поиска"""
        return [
            "email",
            "phone",
            "cancel_reason",
            "cancel_refund_reason",
            "paid_order"
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.user_ids:
            filters.append(ProductOrderEntity.user_id.in_(self.user_ids))

        if self.status_ids:
            filters.append(ProductOrderEntity.status_id.in_(self.status_ids))

        if self.total_price_from is not None:
            filters.append(ProductOrderEntity.total_price >= self.total_price_from)

        if self.total_price_to is not None:
            filters.append(ProductOrderEntity.total_price <= self.total_price_to)

        if self.is_active is not None:
            filters.append(ProductOrderEntity.is_active == self.is_active)

        if self.is_canceled is not None:
            filters.append(ProductOrderEntity.is_canceled == self.is_canceled)

        if self.is_paid is not None:
            filters.append(ProductOrderEntity.is_paid == self.is_paid)

        if self.is_refunded is not None:
            filters.append(ProductOrderEntity.is_refunded == self.is_refunded)

        if self.paid_from is not None:
            filters.append(ProductOrderEntity.paid_at >= self.paid_from)

        if self.paid_to is not None:
            filters.append(ProductOrderEntity.paid_at <= self.paid_to)

        if self.created_from is not None:
            filters.append(ProductOrderEntity.created_at >= self.created_from)

        if self.created_to is not None:
            filters.append(ProductOrderEntity.created_at <= self.created_to)

        return filters