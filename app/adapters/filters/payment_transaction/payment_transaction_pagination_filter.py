from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import PaymentTransactionEntity
from app.shared.query_constants import AppQueryConstants


class PaymentTransactionPaginationFilter(BasePaginationFilter[PaymentTransactionEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество транзакций на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по номеру заказа, описанию, email"
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
            "Фильтрация по статусам"
        ),
        transaction_type: str | None = AppQueryConstants.StandardOptionalStringQuery(
            "Фильтрация по типу транзакции"
        ),
        currency: str | None = AppQueryConstants.StandardOptionalStringQuery(
            "Фильтрация по валюте"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности"
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
            model=PaymentTransactionEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.user_ids = user_ids
        self.status_ids = status_ids
        self.transaction_type = transaction_type
        self.currency = currency
        self.is_active = is_active
        self.is_paid = is_paid
        self.is_canceled = is_canceled
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["order", "mpi_order", "desc", "desc_order", "email", "name"]

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

        if self.transaction_type:
            filters.append(self.model.transaction_type.ilike(f"%{self.transaction_type}%"))

        if self.currency:
            filters.append(self.model.currency.ilike(f"%{self.currency}%"))

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_paid is not None:
            filters.append(self.model.is_paid.is_(self.is_paid))

        if self.is_canceled is not None:
            filters.append(self.model.is_canceled.is_(self.is_canceled))

        return filters