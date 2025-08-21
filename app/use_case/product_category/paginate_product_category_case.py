from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductCategoryWithRelationsRDTO
from app.adapters.dto.product_category.product_category_dto import (
    ProductCategoryWithRelationsRDTO,
)
from app.adapters.filters.product_category.product_category_pagination_filter import (
    ProductCategoryPaginationFilter,
)
from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateProductCategoryCase(
    BaseUseCase[PaginationProductCategoryWithRelationsRDTO]
):
    """
    Класс Use Case для получения пагинированного списка категорий товаров.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ProductCategoryPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.

    Методы:
        execute(filter: ProductCategoryPaginationFilter) -> PaginationProductCategoryWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список категорий товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductCategoryRepository(db)

    async def execute(
        self, filter: ProductCategoryPaginationFilter
    ) -> PaginationProductCategoryWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка категорий товаров.

        Args:
            filter (ProductCategoryPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationProductCategoryWithRelationsRDTO: Объект пагинации с категориями товаров.
        """
        pagination = await self.repository.paginate(
            dto=ProductCategoryWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
