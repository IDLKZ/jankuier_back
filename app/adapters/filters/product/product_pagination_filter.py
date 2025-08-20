from decimal import Decimal
from sqlalchemy import or_, inspect
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import ProductEntity
from app.shared.query_constants import AppQueryConstants


class ProductPaginationFilter(BasePaginationFilter[ProductEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество товаров на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery(
            "Поиск по названию, описанию или артикулу товара"
        ),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        category_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по категориям"),
        city_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по городам"),
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        gender: int | None = AppQueryConstants.StandardOptionalIntegerQuery(
            "Фильтрация по полу: 0-унисекс, 1-мужской, 2-женский"
        ),
        is_for_children: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация детских товаров"
        ),
        is_recommended: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация рекомендованных товаров"
        ),
        is_active: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(
            "Фильтрация по активности товара"
        ),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=ProductEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.category_ids = category_ids
        self.city_ids = city_ids
        self.min_price = min_price
        self.max_price = max_price
        self.gender = gender
        self.is_for_children = is_for_children
        self.is_recommended = is_recommended
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
            "sku",
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

        if self.category_ids:
            filters.append(ProductEntity.category_id.in_(self.category_ids))

        if self.city_ids:
            filters.append(ProductEntity.city_id.in_(self.city_ids))

        if self.min_price is not None:
            filters.append(ProductEntity.base_price >= self.min_price)

        if self.max_price is not None:
            filters.append(ProductEntity.base_price <= self.max_price)

        if self.gender is not None:
            filters.append(ProductEntity.gender == self.gender)

        if self.is_for_children is not None:
            filters.append(self.model.is_for_children.is_(self.is_for_children))

        if self.is_recommended is not None:
            filters.append(self.model.is_recommended.is_(self.is_recommended))

        if self.is_active is not None:
            filters.append(self.model.is_active.is_(self.is_active))

        return filters