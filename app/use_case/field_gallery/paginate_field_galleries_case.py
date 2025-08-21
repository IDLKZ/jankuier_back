from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationFieldGalleryWithRelationsRDTO
from app.adapters.filters.field_gallery.field_gallery_pagination_filter import FieldGalleryPaginationFilter
from app.adapters.repository.field_gallery.field_gallery_repository import FieldGalleryRepository
from app.use_case.base_case import BaseUseCase


class PaginateFieldGalleriesCase(BaseUseCase[PaginationFieldGalleryWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка изображений галереи полей.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - DTO `PaginationFieldGalleryWithRelationsRDTO` для возврата пагинированных данных с связями.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей полей.

    Методы:
        execute() -> PaginationFieldGalleryWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список изображений галереи полей.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldGalleryRepository(db)

    async def execute(self, filter: FieldGalleryPaginationFilter) -> PaginationFieldGalleryWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка изображений галереи полей.

        Args:
            filter (FieldGalleryPaginationFilter): Фильтр для поиска, сортировки и пагинации.

        Returns:
            PaginationFieldGalleryWithRelationsRDTO: Пагинированный список изображений галереи с связями.
        """
        pagination_result = await self.repository.paginate(
            dto=FieldGalleryWithRelationsRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            page=filter.page,
            per_page=filter.per_page,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination_result

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass