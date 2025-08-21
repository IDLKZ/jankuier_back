from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryWithRelationsRDTO
from app.adapters.filters.field_gallery.field_gallery_filter import FieldGalleryFilter
from app.adapters.repository.field_gallery.field_gallery_repository import FieldGalleryRepository
from app.use_case.base_case import BaseUseCase


class AllFieldGalleriesCase(BaseUseCase[list[FieldGalleryWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех изображений галереи полей.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - DTO `FieldGalleryWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей полей.

    Методы:
        execute() -> list[FieldGalleryWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех изображений галереи полей.
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

    async def execute(self, filter: FieldGalleryFilter) -> list[FieldGalleryWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех изображений галереи полей.

        Args:
            filter (FieldGalleryFilter): Фильтр для поиска и сортировки.

        Returns:
            list[FieldGalleryWithRelationsRDTO]: Список объектов изображений галереи с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [FieldGalleryWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass