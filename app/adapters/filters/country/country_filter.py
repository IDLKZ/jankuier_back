from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import CountryEntity
from app.shared.query_constants import AppQueryConstants


class CountryFilter(BaseFilter[CountryEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию страны"
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
            model=CountryEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title_ru", "title_kk", "title_en", "sota_code", "sota_flag_image"]

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

        return filters