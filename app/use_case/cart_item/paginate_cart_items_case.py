from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import (
    CartItemWithRelationsRDTO,
    PaginationCartItemWithRelationsRDTO,
)
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.use_case.base_case import BaseUseCase


class PaginateCartItemsCase(BaseUseCase[PaginationCartItemWithRelationsRDTO]):
    """
    Класс Use Case для получения товаров в корзинах с пагинацией.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.
        - Фильтр `PaginationFilter` для применения условий поиска, сортировки и пагинации.
        - DTO `PaginationCartItemWithRelationsRDTO` для возврата данных с пагинацией.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.

    Методы:
        execute(filter: BasePaginationFilter) -> PaginationCartItemWithRelationsRDTO:
            Выполняет запрос и возвращает товары в корзинах с пагинацией.
        validate(filter: BasePaginationFilter):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)

    async def execute(
        self, filter: BasePaginationFilter
    ) -> PaginationCartItemWithRelationsRDTO:
        """
        Выполняет операцию получения товаров в корзинах с пагинацией.

        Args:
            filter (PaginationFilter): Объект фильтра с параметрами поиска, сортировки и пагинации.

        Returns:
            PaginationCartItemWithRelationsRDTO: Пагинированный список товаров в корзинах с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по SKU, названию товара, цене или количеству
            filters.append(
                or_(
                    func.lower(self.repository.model.sku).like(search_term),
                    func.lower(self.repository.model.product.title_ru).like(
                        search_term
                    ),
                    func.lower(self.repository.model.product.title_kk).like(
                        search_term
                    ),
                    func.lower(self.repository.model.product.title_en).like(
                        search_term
                    ),
                    func.cast(self.repository.model.unit_price, func.text("TEXT")).like(
                        search_term
                    ),
                    func.cast(
                        self.repository.model.total_price, func.text("TEXT")
                    ).like(search_term),
                    func.cast(self.repository.model.qty, func.text("TEXT")).like(
                        search_term
                    ),
                )
            )

        # Получаем данные из репозитория с пагинацией
        result = await self.repository.paginate(
            dto=CartItemWithRelationsRDTO,
            filters=filters,
            page=filter.page,
            per_page=filter.per_page,
            order_by=getattr(filter, "order_by", "created_at"),
            order_direction=getattr(filter, "order_direction", "desc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return result

    async def validate(self, filter: BasePaginationFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (PaginationFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
