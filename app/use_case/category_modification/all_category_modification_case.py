from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.category_modification.category_modification_dto import (
    CategoryModificationWithRelationsRDTO,
)
from app.adapters.filters.category_modification.category_modification_filter import (
    CategoryModificationFilter,
)
from app.adapters.repository.category_modification.category_modification_repository import (
    CategoryModificationRepository,
)
from app.use_case.base_case import BaseUseCase


class AllCategoryModificationCase(
    BaseUseCase[list[CategoryModificationWithRelationsRDTO]]
):
    """
    Класс Use Case для получения списка всех модификаций категорий.

    Использует:
        - Репозиторий `CategoryModificationRepository` для работы с базой данных.
        - DTO `CategoryModificationWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (CategoryModificationRepository): Репозиторий для работы с модификациями категорий.

    Методы:
        execute(filter: CategoryModificationFilter) -> list[CategoryModificationWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех модификаций категорий.
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
        self, filter: CategoryModificationFilter
    ) -> list[CategoryModificationWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех модификаций категорий.

        Args:
            filter (CategoryModificationFilter): Фильтр для поиска и сортировки модификаций категорий.

        Returns:
            list[CategoryModificationWithRelationsRDTO]: Список объектов модификаций категорий с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [
            CategoryModificationWithRelationsRDTO.from_orm(model) for model in models
        ]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
