from sqlalchemy import func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_gallery.academy_gallery_dto import AcademyGalleryWithRelationsRDTO
from app.adapters.filter.base_filter import BaseFilter
from app.adapters.repository.academy_gallery.academy_gallery_repository import AcademyGalleryRepository
from app.use_case.base_case import BaseUseCase


class AllAcademyGalleriesCase(BaseUseCase[list[AcademyGalleryWithRelationsRDTO]]):
    """
    Класс Use Case для получения всех изображений галереи академий с фильтрацией.

    Использует:
        - Репозиторий `AcademyGalleryRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `AcademyGalleryWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGalleryRepository): Репозиторий для работы с галереей академий.

    Методы:
        execute(filter: BaseFilter) -> list[AcademyGalleryWithRelationsRDTO]:
            Выполняет запрос и возвращает список изображений галереи.
        validate(filter: BaseFilter):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGalleryRepository(db)

    async def execute(self, filter: BaseFilter) -> list[AcademyGalleryWithRelationsRDTO]:
        """
        Выполняет операцию получения всех изображений галереи академий с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[AcademyGalleryWithRelationsRDTO]: Список изображений галереи с связями.
        """
        await self.validate(filter)
        
        # Применяем фильтры
        filters = []
        if hasattr(filter, 'search') and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по полям связанных сущностей
            filters.append(
                or_(
                    func.lower(self.repository.model.academy.title_ru).like(search_term),
                    func.lower(self.repository.model.academy.title_kk).like(search_term),
                    func.lower(self.repository.model.academy.title_en).like(search_term),
                    func.lower(self.repository.model.group.name).like(search_term),
                    func.lower(self.repository.model.file.filename).like(search_term),
                )
            )
        
        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, 'order_by', 'created_at'),
            order_direction=getattr(filter, 'order_direction', 'desc'),
            include_deleted_filter=not getattr(filter, 'is_show_deleted', False),
            options=self.repository.default_relationships(),
        )
        
        return [AcademyGalleryWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self, filter: BaseFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (BaseFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass