from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_gallery.product_gallery_dto import (
    ProductGalleryWithRelationsRDTO,
)
from app.adapters.filters.product_gallery.product_gallery_filter import (
    ProductGalleryFilter,
)
from app.adapters.repository.product_gallery.product_gallery_repository import (
    ProductGalleryRepository,
)
from app.use_case.base_case import BaseUseCase


class AllProductGalleryCase(BaseUseCase[list[ProductGalleryWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех изображений галереи товаров.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - DTO `ProductGalleryWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.

    Методы:
        execute(filter: ProductGalleryFilter) -> list[ProductGalleryWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех изображений галереи товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductGalleryRepository(db)

    async def execute(
        self, filter: ProductGalleryFilter
    ) -> list[ProductGalleryWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех изображений галереи товаров.

        Args:
            filter (ProductGalleryFilter): Фильтр для поиска и сортировки изображений галереи товаров.

        Returns:
            list[ProductGalleryWithRelationsRDTO]: Список объектов изображений галереи товаров с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ProductGalleryWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
