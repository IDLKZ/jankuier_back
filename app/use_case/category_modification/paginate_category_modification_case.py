from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import (
    PaginationCategoryModificationWithRelationsRDTO,
)
from app.adapters.dto.category_modification.category_modification_dto import (
    CategoryModificationWithRelationsRDTO,
)
from app.adapters.filters.category_modification.category_modification_pagination_filter import (
    CategoryModificationPaginationFilter,
)
from app.adapters.repository.category_modification.category_modification_repository import (
    CategoryModificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateCategoryModificationCase(
    BaseUseCase[PaginationCategoryModificationWithRelationsRDTO]
):
    """
    Класс Use Case для получения пагинированного списка модификаций категорий.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.
        - DTO `CategoryModificationWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `CategoryModificationPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.

    Методы:
        execute(filter: CategoryModificationPaginationFilter) -> PaginationCategoryModificationWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список модификаций категорий.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CategoryModificationRepository(db)

    async def execute(
        self, filter: CategoryModificationPaginationFilter
    ) -> PaginationCategoryModificationWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка модификаций категорий.

        Args:
            filter (CategoryModificationPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationCategoryModificationWithRelationsRDTO: Объект пагинации с модификациями категорий.
        """
        pagination = await self.repository.paginate(
            dto=CategoryModificationWithRelationsRDTO,
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
