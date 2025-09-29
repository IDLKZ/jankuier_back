from datetime import datetime
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import ProductOrderItemEntity
from app.shared.query_constants import AppQueryConstants


class ProductOrderItemPaginationFilter(BasePaginationFilter[ProductOrderItemEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество элементов заказа на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по SKU, причине отмены"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        order_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по заказам"
        ),
        status_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по статусам элементов заказа"
        ),
        product_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по товарам"
        ),
        variant_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по вариантам товаров"
        ),
        from_city_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по городам отправления"
        ),
        to_city_ids: list[int] | None = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по городам получения"
        ),
        total_price_from: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Общая стоимость элемента от"
        ),
        total_price_to: float | None = AppQueryConstants.StandardOptionalDecimalQuery(
            "Общая стоимость элемента до"
        ),
        qty_from: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Количество от"
        ),
        qty_to: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Количество до"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активным элементам"
        ),
        is_canceled: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по отмененным элементам"
        ),
        is_paid: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по оплаченным элементам"
        ),
        is_refunded: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по возвращенным элементам"
        ),
        delivery_from: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата доставки от"
        ),
        delivery_to: datetime | None = AppQueryConstants.StandardOptionalDateTimeQuery(
            "Дата доставки до"
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
            model=ProductOrderItemEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.order_ids = order_ids
        self.status_ids = status_ids
        self.product_ids = product_ids
        self.variant_ids = variant_ids
        self.from_city_ids = from_city_ids
        self.to_city_ids = to_city_ids
        self.total_price_from = total_price_from
        self.total_price_to = total_price_to
        self.qty_from = qty_from
        self.qty_to = qty_to
        self.is_active = is_active
        self.is_canceled = is_canceled
        self.is_paid = is_paid
        self.is_refunded = is_refunded
        self.delivery_from = delivery_from
        self.delivery_to = delivery_to
        self.created_from = created_from
        self.created_to = created_to
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        """Поля для текстового поиска"""
        return [
            "sku",
            "cancel_reason",
            "cancel_refund_reason"
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.order_ids:
            filters.append(ProductOrderItemEntity.order_id.in_(self.order_ids))

        if self.status_ids:
            filters.append(ProductOrderItemEntity.status_id.in_(self.status_ids))

        if self.product_ids:
            filters.append(ProductOrderItemEntity.product_id.in_(self.product_ids))

        if self.variant_ids:
            filters.append(ProductOrderItemEntity.variant_id.in_(self.variant_ids))

        if self.from_city_ids:
            filters.append(ProductOrderItemEntity.from_city_id.in_(self.from_city_ids))

        if self.to_city_ids:
            filters.append(ProductOrderItemEntity.to_city_id.in_(self.to_city_ids))

        if self.total_price_from is not None:
            filters.append(ProductOrderItemEntity.total_price >= self.total_price_from)

        if self.total_price_to is not None:
            filters.append(ProductOrderItemEntity.total_price <= self.total_price_to)

        if self.qty_from is not None:
            filters.append(ProductOrderItemEntity.qty >= self.qty_from)

        if self.qty_to is not None:
            filters.append(ProductOrderItemEntity.qty <= self.qty_to)

        if self.is_active is not None:
            filters.append(ProductOrderItemEntity.is_active == self.is_active)

        if self.is_canceled is not None:
            filters.append(ProductOrderItemEntity.is_canceled == self.is_canceled)

        if self.is_paid is not None:
            filters.append(ProductOrderItemEntity.is_paid == self.is_paid)

        if self.is_refunded is not None:
            filters.append(ProductOrderItemEntity.is_refunded == self.is_refunded)

        if self.delivery_from is not None:
            filters.append(ProductOrderItemEntity.delivery_date >= self.delivery_from)

        if self.delivery_to is not None:
            filters.append(ProductOrderItemEntity.delivery_date <= self.delivery_to)

        if self.created_from is not None:
            filters.append(ProductOrderItemEntity.created_at >= self.created_from)

        if self.created_to is not None:
            filters.append(ProductOrderItemEntity.created_at <= self.created_to)

        return filters