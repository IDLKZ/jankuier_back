from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_type.modification_type_dto import (
    ModificationTypeRDTO,
)
from app.adapters.filters.modification_type.modification_type_filter import (
    ModificationTypeFilter,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.use_case.base_case import BaseUseCase


class AllModificationTypeCase(BaseUseCase[list[ModificationTypeRDTO]]):
    """
    Класс Use Case для получения списка всех типов модификаций.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeRDTO` для возврата данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.

    Методы:
        execute(filter: ModificationTypeFilter) -> list[ModificationTypeRDTO]:
            Выполняет запрос и возвращает список всех типов модификаций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)

    async def execute(
        self, filter: ModificationTypeFilter
    ) -> list[ModificationTypeRDTO]:
        """
        Выполняет операцию получения списка всех типов модификаций.

        Args:
            filter (ModificationTypeFilter): Фильтр для поиска и сортировки типов модификаций.

        Returns:
            list[ModificationTypeRDTO]: Список объектов типов модификаций.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ModificationTypeRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
