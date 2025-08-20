from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import ProductCategoryEntity
from app.shared.query_constants import AppQueryConstants


class ProductCategoryPaginationFilter(BasePaginationFilter[ProductCategoryEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество категорий на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию категории товара"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности категории"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductCategoryEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.is_active = is_active
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return [
            "title_ru",
            "title_kk", 
            "title_en",
            "description_ru",
            "description_kk",
            "description_en",
            "value"
        ]

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

        return filters