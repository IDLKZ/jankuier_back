from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_category.product_category_dto import (
    ProductCategoryWithRelationsRDTO,
)
from app.adapters.filters.product_category.product_category_filter import (
    ProductCategoryFilter,
)
from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.use_case.base_case import BaseUseCase


class AllProductCategoryCase(BaseUseCase[list[ProductCategoryWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех категорий товаров.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - DTO `ProductCategoryWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.

    Методы:
        execute(filter: ProductCategoryFilter) -> list[ProductCategoryWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех категорий товаров.
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
        self, filter: ProductCategoryFilter
    ) -> list[ProductCategoryWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех категорий товаров.

        Args:
            filter (ProductCategoryFilter): Фильтр для поиска и сортировки категорий товаров.

        Returns:
            list[ProductCategoryWithRelationsRDTO]: Список объектов категорий товаров с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ProductCategoryWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
