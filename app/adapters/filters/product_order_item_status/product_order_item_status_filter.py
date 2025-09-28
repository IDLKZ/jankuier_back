from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery
from app.adapters.filters.base_filter import BaseFilter
from app.entities import ProductOrderItemStatusEntity
from app.shared.query_constants import AppQueryConstants


class ProductOrderItemStatusFilter(BaseFilter[ProductOrderItemStatusEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию статуса элемента заказа"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности статуса"
        ),
        is_first: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по первому статусу"
        ),
        is_last: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по последнему статусу"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductOrderItemStatusEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_active = is_active
        self.is_first = is_first
        self.is_last = is_last
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title_ru", "title_kk", "title_en"]

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

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_first is not None:
            filters.append(self.model.is_first.is_(self.is_first))

        if self.is_last is not None:
            filters.append(self.model.is_last.is_(self.is_last))

        return filters