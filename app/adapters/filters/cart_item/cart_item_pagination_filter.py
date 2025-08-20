from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import CartItemEntity
from app.shared.query_constants import AppQueryConstants


class CartItemPaginationFilter(BasePaginationFilter[CartItemEntity]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(
            "Количество позиций корзины на странице"
        ),
        page: int = AppQueryConstants.StandardPageQuery("Номер страницы"),
        search: str | None = AppQueryConstants.StandardOptionalSearchQuery("Поиск по SKU товара"),
        order_by: str | None = AppQueryConstants.StandardSortFieldQuery(
            "Поле сортировки"
        ),
        order_direction: str | None = AppQueryConstants.StandardSortDirectionQuery(
            "Направление сортировки"
        ),
        cart_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по корзинам"),
        product_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по товарам"),
        variant_ids: (
            list[int] | None
        ) = AppQueryConstants.StandardOptionalIntegerArrayQuery("Фильтрация по вариантам товаров"),
        qty_from: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Количество товара от"),
        qty_to: (
            int | None
        ) = AppQueryConstants.StandardOptionalIntegerQuery("Количество товара до"),
        unit_price_from: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Цена за единицу от"),
        unit_price_to: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Цена за единицу до"),
        total_price_from: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Общая стоимость позиции от"),
        total_price_to: (
            float | None
        ) = AppQueryConstants.StandardOptionalDecimalQuery("Общая стоимость позиции до"),
        has_variant: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по наличию варианта товара"),
        has_discount: (
            bool | None
        ) = AppQueryConstants.StandardOptionalBooleanQuery("Фильтрация по наличию скидки (отрицательная delta_price)"),
        is_show_deleted: bool = AppQueryConstants.StandardBooleanQuery(
            "Показывать удаленные данные?"
        ),
    ) -> None:
        super().__init__(
            model=CartItemEntity,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.cart_ids = cart_ids
        self.product_ids = product_ids
        self.variant_ids = variant_ids
        self.qty_from = qty_from
        self.qty_to = qty_to
        self.unit_price_from = unit_price_from
        self.unit_price_to = unit_price_to
        self.total_price_from = total_price_from
        self.total_price_to = total_price_to
        self.has_variant = has_variant
        self.has_discount = has_discount
        self.is_show_deleted = is_show_deleted

    def get_search_filters(self) -> list[str] | None:
        return ["sku"]

    def apply(self) -> list[SQLAlchemyQuery]:
        filters = []

        if self.cart_ids:
            filters.append(CartItemEntity.cart_id.in_(self.cart_ids))

        if self.product_ids:
            filters.append(CartItemEntity.product_id.in_(self.product_ids))

        if self.variant_ids:
            filters.append(CartItemEntity.variant_id.in_(self.variant_ids))

        if self.qty_from is not None:
            filters.append(CartItemEntity.qty >= self.qty_from)

        if self.qty_to is not None:
            filters.append(CartItemEntity.qty <= self.qty_to)

        if self.unit_price_from is not None:
            filters.append(CartItemEntity.unit_price >= self.unit_price_from)

        if self.unit_price_to is not None:
            filters.append(CartItemEntity.unit_price <= self.unit_price_to)

        if self.total_price_from is not None:
            filters.append(CartItemEntity.total_price >= self.total_price_from)

        if self.total_price_to is not None:
            filters.append(CartItemEntity.total_price <= self.total_price_to)

        if self.has_variant is not None:
            if self.has_variant:
                filters.append(CartItemEntity.variant_id.is_not(None))
            else:
                filters.append(CartItemEntity.variant_id.is_(None))

        if self.has_discount is not None:
            if self.has_discount:
                filters.append(CartItemEntity.delta_price < 0)
            else:
                filters.append(CartItemEntity.delta_price >= 0)

        return filters