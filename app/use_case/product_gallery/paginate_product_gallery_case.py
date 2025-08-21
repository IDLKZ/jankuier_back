from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductGalleryWithRelationsRDTO
from app.adapters.dto.product_gallery.product_gallery_dto import (
    ProductGalleryWithRelationsRDTO,
)
from app.adapters.filters.product_gallery.product_gallery_pagination_filter import (
    ProductGalleryPaginationFilter,
)
from app.adapters.repository.product_gallery.product_gallery_repository import (
    ProductGalleryRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateProductGalleryCase(
    BaseUseCase[PaginationProductGalleryWithRelationsRDTO]
):
    """
    Класс Use Case для получения пагинированного списка изображений галереи товаров.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - DTO `ProductGalleryWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `ProductGalleryPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.

    Методы:
        execute(filter: ProductGalleryPaginationFilter) -> PaginationProductGalleryWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список изображений галереи товаров.
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
        self, filter: ProductGalleryPaginationFilter
    ) -> PaginationProductGalleryWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка изображений галереи товаров.

        Args:
            filter (ProductGalleryPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationProductGalleryWithRelationsRDTO: Объект пагинации с изображениями галереи товаров.
        """
        pagination = await self.repository.paginate(
            dto=ProductGalleryWithRelationsRDTO,
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
