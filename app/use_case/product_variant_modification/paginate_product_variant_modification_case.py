from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import (
    PaginationProductVariantModificationWithRelationsRDTO,
)
from app.adapters.dto.product_variant_modification.product_variant_modification_dto import (
    ProductVariantModificationWithRelationsRDTO,
)
from app.adapters.filters.product_variant_modification.product_variant_modification_pagination_filter import (
    ProductVariantModificationPaginationFilter,
)
from app.adapters.repository.product_variant_modification.product_variant_modification_repository import (
    ProductVariantModificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateProductVariantModificationCase(
    BaseUseCase[PaginationProductVariantModificationWithRelationsRDTO]
):
    """
    Класс Use Case для получения пагинированного списка модификаций вариантов товаров.

    Использует:
        - Репозиторий `ProductVariantModificationRepository` для работы с базой данных.
        - DTO `ProductVariantModificationWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ProductVariantModificationPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ProductVariantModificationRepository): Репозиторий для работы с модификациями вариантов товаров.

    Методы:
        execute(filter: ProductVariantModificationPaginationFilter) -> PaginationProductVariantModificationWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список модификаций вариантов товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantModificationRepository(db)

    async def execute(
        self, filter: ProductVariantModificationPaginationFilter
    ) -> PaginationProductVariantModificationWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка модификаций вариантов товаров.

        Args:
            filter (ProductVariantModificationPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationProductVariantModificationWithRelationsRDTO: Объект пагинации с модификациями вариантов товаров.
        """
        pagination = await self.repository.paginate(
            dto=ProductVariantModificationWithRelationsRDTO,
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
