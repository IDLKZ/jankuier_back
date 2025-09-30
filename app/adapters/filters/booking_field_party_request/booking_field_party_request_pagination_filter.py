from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import BookingFieldPartyRequestEntity
from app.shared.query_constants import AppQueryConstants


class BookingFieldPartyRequestPaginationFilter(BasePaginationFilter[BookingFieldPartyRequestEntity]):
    """
    Пагинационный фильтр для бронирований площадок.

    Поддерживает фильтрацию по:
    - Поиску по email, phone, cancel_reason
    - ID пользователей, статусов, площадок, мероприятий
    - Флагам: is_active, is_canceled, is_paid, is_refunded
    - Пагинацию: page, per_page
    """

    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество бронирований на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по email, телефону, причине отмены"
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
            "Фильтрация по статусам бронирования"
        ),
        field_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по площадкам"
        ),
        field_party_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по групповым мероприятиям"
        ),
        payment_transaction_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по транзакциям"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности бронирования"
        ),
        is_canceled: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу отмены"
        ),
        is_paid: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу оплаты"
        ),
        is_refunded: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по статусу возврата"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=BookingFieldPartyRequestEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.user_ids = user_ids
        self.status_ids = status_ids
        self.field_ids = field_ids
        self.field_party_ids = field_party_ids
        self.payment_transaction_ids = payment_transaction_ids
        self.is_active = is_active
        self.is_canceled = is_canceled
        self.is_paid = is_paid
        self.is_refunded = is_refunded
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        """Поля для поиска по тексту"""
        return ["email", "phone", "cancel_reason", "cancel_refund_reason", "paid_order"]

    def apply(self) -> list[SQLAlchemyQuery]:
        """Применяет фильтры к запросу"""
        filters = []

        # Поиск по текстовым полям
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

        # Фильтрация по ID
        if self.user_ids:
            filters.append(self.model.user_id.in_(self.user_ids))

        if self.status_ids:
            filters.append(self.model.status_id.in_(self.status_ids))

        if self.field_ids:
            filters.append(self.model.field_id.in_(self.field_ids))

        if self.field_party_ids:
            filters.append(self.model.field_party_id.in_(self.field_party_ids))

        if self.payment_transaction_ids:
            filters.append(self.model.payment_transaction_id.in_(self.payment_transaction_ids))

        # Фильтрация по флагам
        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_canceled is not None:
            filters.append(self.model.is_canceled.is_(self.is_canceled))

        if self.is_paid is not None:
            filters.append(self.model.is_paid.is_(self.is_paid))

        if self.is_refunded is not None:
            filters.append(self.model.is_refunded.is_(self.is_refunded))

        return filters