from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant_modification.product_variant_modification_dto import (
    ProductVariantModificationWithRelationsRDTO,
)
from app.adapters.filters.product_variant_modification.product_variant_modification_filter import (
    ProductVariantModificationFilter,
)
from app.adapters.repository.product_variant_modification.product_variant_modification_repository import (
    ProductVariantModificationRepository,
)
from app.use_case.base_case import BaseUseCase


class AllProductVariantModificationCase(
    BaseUseCase[list[ProductVariantModificationWithRelationsRDTO]]
):
    """
    Класс Use Case для получения списка всех модификаций вариантов товаров.

    Использует:
        - Репозиторий `ProductVariantModificationRepository` для работы с базой данных.
        - DTO `ProductVariantModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductVariantModificationRepository): Репозиторий для работы с модификациями вариантов товаров.

    Методы:
        execute(filter: ProductVariantModificationFilter) -> list[ProductVariantModificationWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех модификаций вариантов товаров.
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
        self, filter: ProductVariantModificationFilter
    ) -> list[ProductVariantModificationWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех модификаций вариантов товаров.

        Args:
            filter (ProductVariantModificationFilter): Фильтр для поиска и сортировки модификаций вариантов товаров.

        Returns:
            list[ProductVariantModificationWithRelationsRDTO]: Список объектов модификаций вариантов товаров с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [
            ProductVariantModificationWithRelationsRDTO.from_orm(model)
            for model in models
        ]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
