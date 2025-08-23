from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_gallery.academy_gallery_dto import (
    AcademyGalleryWithRelationsRDTO,
    PaginationAcademyGalleryWithRelationsRDTO,
)
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.adapters.repository.academy_gallery.academy_gallery_repository import (
    AcademyGalleryRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateAcademyGalleriesCase(
    BaseUseCase[PaginationAcademyGalleryWithRelationsRDTO]
):
    """
    Класс Use Case для получения изображений галереи академий с пагинацией.

    Использует:
        - Репозиторий `AcademyGalleryRepository` для работы с базой данных.
        - Фильтр `PaginationFilter` для применения условий поиска, сортировки и пагинации.
        - DTO `PaginationAcademyGalleryWithRelationsRDTO` для возврата данных с пагинацией.

    Атрибуты:
        repository (AcademyGalleryRepository): Репозиторий для работы с галереей академий.

    Методы:
        execute(filter: BasePaginationFilter) -> PaginationAcademyGalleryWithRelationsRDTO:
            Выполняет запрос и возвращает изображения галереи с пагинацией.
        validate(filter: BasePaginationFilter):
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

    async def execute(
        self, filter: BasePaginationFilter
    ) -> PaginationAcademyGalleryWithRelationsRDTO:
        """
        Выполняет операцию получения изображений галереи академий с пагинацией.

        Args:
            filter (PaginationFilter): Объект фильтра с параметрами поиска, сортировки и пагинации.

        Returns:
            PaginationAcademyGalleryWithRelationsRDTO: Пагинированный список изображений галереи с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по полям связанных сущностей
            filters.append(
                or_(
                    func.lower(self.repository.model.academy.title_ru).like(
                        search_term
                    ),
                    func.lower(self.repository.model.academy.title_kk).like(
                        search_term
                    ),
                    func.lower(self.repository.model.academy.title_en).like(
                        search_term
                    ),
                    func.lower(self.repository.model.group.name).like(search_term),
                    func.lower(self.repository.model.file.filename).like(search_term),
                )
            )

        # Получаем данные из репозитория с пагинацией
        result = await self.repository.paginate(
            dto=AcademyGalleryWithRelationsRDTO,
            filters=filters,
            page=filter.page,
            per_page=filter.per_page,
            order_by=getattr(filter, "order_by", "created_at"),
            order_direction=getattr(filter, "order_direction", "desc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return result

    async def validate(self, filter: BasePaginationFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (PaginationFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
