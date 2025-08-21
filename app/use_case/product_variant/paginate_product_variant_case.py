from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductVariantWithRelationsRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantWithRelationsRDTO
from app.adapters.filters.product_variant.product_variant_pagination_filter import ProductVariantPaginationFilter
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.use_case.base_case import BaseUseCase


class PaginateProductVariantCase(BaseUseCase[PaginationProductVariantWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка вариантов товаров.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - DTO `ProductVariantWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ProductVariantPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.

    Методы:
        execute(filter: ProductVariantPaginationFilter) -> PaginationProductVariantWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список вариантов товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantRepository(db)

    async def execute(self, filter: ProductVariantPaginationFilter) -> PaginationProductVariantWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка вариантов товаров.

        Args:
            filter (ProductVariantPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationProductVariantWithRelationsRDTO: Объект пагинации с вариантами товаров.
        """
        pagination = await self.repository.paginate(
            dto=ProductVariantWithRelationsRDTO,
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