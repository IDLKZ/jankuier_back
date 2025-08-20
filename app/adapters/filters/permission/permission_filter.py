from sqlalchemy import inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import PermissionEntity
from app.shared.query_constants import AppQueryConstants


class PermissionFilter(BaseFilter[PermissionEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию или значению"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=PermissionEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "title_ru",
            "title_kk",
            "title_en",
            "value",
        ]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.search:
            model_columns = {column.key for column in inspect(self.model).columns}
            valid_fields = [f for f in self.get_search_filters() if f in model_columns]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).ilike(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )

        return filters
