from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductWithRelationsRDTO
from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.filters.product.product_pagination_filter import (
    ProductPaginationFilter,
)
from app.adapters.repository.product.product_repository import ProductRepository
from app.use_case.base_case import BaseUseCase


class PaginateProductCase(BaseUseCase[PaginationProductWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка товаров.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ProductPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.

    Методы:
        execute(filter: ProductPaginationFilter) -> PaginationProductWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)

    async def execute(
        self, filter: ProductPaginationFilter
    ) -> PaginationProductWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка товаров.

        Args:
            filter (ProductPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationProductWithRelationsRDTO: Объект пагинации с товарами.
        """
        pagination = await self.repository.paginate(
            dto=ProductWithRelationsRDTO,
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
