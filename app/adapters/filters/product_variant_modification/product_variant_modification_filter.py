from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import ProductVariantModificationEntity
from app.shared.query_constants import AppQueryConstants


class ProductVariantModificationFilter(BaseFilter[ProductVariantModificationEntity]):
    def __init__(
        self,
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        variant_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по вариантам товара"),
        modification_value_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по значениям модификаций"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductVariantModificationEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
        )
        self.variant_ids = variant_ids
        self.modification_value_ids = modification_value_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.variant_ids:
            filters.append(ProductVariantModificationEntity.variant_id.in_(self.variant_ids))

        if self.modification_value_ids:
            filters.append(ProductVariantModificationEntity.modification_value_id.in_(self.modification_value_ids))

        return filters