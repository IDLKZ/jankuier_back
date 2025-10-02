from sqlalchemy import and_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import ProductGalleryEntity
from app.shared.query_constants import AppQueryConstants


class ProductGalleryPaginationFilter(BasePaginationFilter[ProductGalleryEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество изображений галереи товаров на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        product_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по товарам"
        ),
        variant_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery(
            "Фильтрация по вариантам товаров"
        ),
        file_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по файлам"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductGalleryEntity,
            search=None,  # В таблице нет строковых полей для поиска
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.product_ids = product_ids
        self.variant_ids = variant_ids
        self.file_ids = file_ids
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return []  # В таблице нет строковых полей для текстового поиска

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.product_ids and not self.variant_ids:
            filters.append(
                and_(ProductGalleryEntity.product_id.in_(self.product_ids), ProductGalleryEntity.variant_id.is_(None))
            )

        if self.variant_ids:
            filters.append(ProductGalleryEntity.variant_id.in_(self.variant_ids))

        if self.file_ids:
            filters.append(ProductGalleryEntity.file_id.in_(self.file_ids))

        return filters
