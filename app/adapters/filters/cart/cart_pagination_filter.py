from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import CartEntity
from app.shared.query_constants import AppQueryConstants


class CartPaginationFilter(BasePaginationFilter[CartEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество корзин на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        user_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по пользователям"),
        total_price_from: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Общая стоимость корзины от"),
        total_price_to: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Общая стоимость корзины до"),
        has_items: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по наличию товаров в корзине"),
        is_empty: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по пустой корзине"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=CartEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.user_ids = user_ids
        self.total_price_from = total_price_from
        self.total_price_to = total_price_to
        self.has_items = has_items
        self.is_empty = is_empty
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.user_ids:
            filters.append(CartEntity.user_id.in_(self.user_ids))

        if self.total_price_from is not None:
            filters.append(CartEntity.total_price >= self.total_price_from)

        if self.total_price_to is not None:
            filters.append(CartEntity.total_price <= self.total_price_to)

        if self.has_items is not None:
            if self.has_items:
                filters.append(CartEntity.total_price > 0)
            else:
                filters.append(CartEntity.total_price == 0)

        if self.is_empty is not None:
            if self.is_empty:
                filters.append(CartEntity.total_price == 0)
            else:
                filters.append(CartEntity.total_price > 0)

        return filters