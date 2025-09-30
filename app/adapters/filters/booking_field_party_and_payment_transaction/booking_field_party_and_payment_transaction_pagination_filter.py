from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import BookingFieldPartyAndPaymentTransactionEntity
from app.shared.query_constants import AppQueryConstants


class BookingFieldPartyAndPaymentTransactionPaginationFilter(BasePaginationFilter[BookingFieldPartyAndPaymentTransactionEntity]):
    """
    Пагинационный фильтр для связей между бронированиями площадок и платежными транзакциями.

    Поддерживает фильтрацию по:
    - Поиску по типу связи, причине связи
    - ID бронирований и транзакций
    - Флагам: is_active, is_primary
    - Типу связи
    - Пагинацию: page, per_page
    """

    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество связей на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по типу связи и причине"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        request_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по бронированиям"
        ),
        payment_transaction_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по транзакциям"
        ),
        link_types: (
            list[str] | None
        ) = AppQueryConstants.StandardOptionalStringArrayQuery(
            "Фильтрация по типам связи"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности связи"
        ),
        is_primary: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по основным транзакциям"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=BookingFieldPartyAndPaymentTransactionEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.request_ids = request_ids
        self.payment_transaction_ids = payment_transaction_ids
        self.link_types = link_types
        self.is_active = is_active
        self.is_primary = is_primary
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        """Поля для поиска по тексту"""
        return ["link_type", "link_reason"]

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
        if self.request_ids:
            filters.append(self.model.request_id.in_(self.request_ids))

        if self.payment_transaction_ids:
            filters.append(self.model.payment_transaction_id.in_(self.payment_transaction_ids))

        # Фильтрация по типам связи
        if self.link_types:
            filters.append(self.model.link_type.in_(self.link_types))

        # Фильтрация по флагам
        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_primary is not None:
            filters.append(self.model.is_primary.is_(self.is_primary))

        return filters