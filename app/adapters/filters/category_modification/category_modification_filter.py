from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import CategoryModificationEntity
from app.shared.query_constants import AppQueryConstants


class CategoryModificationFilter(BaseFilter[CategoryModificationEntity]):
    def __init__(
        self,
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        category_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по категориям товаров"
        ),
        modification_type_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по типам модификаций"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=CategoryModificationEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
        )
        self.category_ids = category_ids
        self.modification_type_ids = modification_type_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.category_ids:
            filters.append(
                CategoryModificationEntity.category_id.in_(self.category_ids)
            )

        if self.modification_type_ids:
            filters.append(
                CategoryModificationEntity.modification_type_id.in_(
                    self.modification_type_ids
                )
            )

        return filters
