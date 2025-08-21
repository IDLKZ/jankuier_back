from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant.product_variant_dto import (
    ProductVariantWithRelationsRDTO,
)
from app.adapters.filters.product_variant.product_variant_filter import (
    ProductVariantFilter,
)
from app.adapters.repository.product_variant.product_variant_repository import (
    ProductVariantRepository,
)
from app.use_case.base_case import BaseUseCase


class AllProductVariantCase(BaseUseCase[list[ProductVariantWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех вариантов товаров.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - DTO `ProductVariantWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.

    Методы:
        execute(filter: ProductVariantFilter) -> list[ProductVariantWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех вариантов товаров.
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

    async def execute(
        self, filter: ProductVariantFilter
    ) -> list[ProductVariantWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех вариантов товаров.

        Args:
            filter (ProductVariantFilter): Фильтр для поиска и сортировки вариантов товаров.

        Returns:
            list[ProductVariantWithRelationsRDTO]: Список объектов вариантов товаров с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ProductVariantWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
