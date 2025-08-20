from decimal import Decimal
from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_filter import BaseFilter
from app.entities import ProductVariantEntity
from app.shared.query_constants import AppQueryConstants


class ProductVariantFilter(BaseFilter[ProductVariantEntity]):
    def __init__(
        self,
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию или артикулу варианта товара"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        product_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по товарам"),
        city_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по городам"),
        min_stock: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Минимальное количество на складе"
        ),
        max_stock: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Максимальное количество на складе"
        ),
        min_price_delta: Decimal | None = None,
        max_price_delta: Decimal | None = None,
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности варианта"
        ),
        is_default: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по варианту по умолчанию"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductVariantEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )
        self.product_ids = product_ids
        self.city_ids = city_ids
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.min_price_delta = min_price_delta
        self.max_price_delta = max_price_delta
        self.is_active = is_active
        self.is_default = is_default
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["title_ru", "title_kk", "title_en", "value", "sku"]

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

        if self.product_ids:
            filters.append(ProductVariantEntity.product_id.in_(self.product_ids))

        if self.city_ids:
            filters.append(ProductVariantEntity.city_id.in_(self.city_ids))

        if self.min_stock is not None:
            filters.append(ProductVariantEntity.stock >= self.min_stock)

        if self.max_stock is not None:
            filters.append(ProductVariantEntity.stock <= self.max_stock)

        if self.min_price_delta is not None:
            filters.append(ProductVariantEntity.price_delta >= self.min_price_delta)

        if self.max_price_delta is not None:
            filters.append(ProductVariantEntity.price_delta <= self.max_price_delta)

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        if self.is_default is not None:
            filters.append(self.model.is_default.is_(self.is_default))

        return filters