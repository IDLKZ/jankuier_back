from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO
from app.adapters.filters.modification_value.modification_value_filter import ModificationValueFilter
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.use_case.base_case import BaseUseCase


class AllModificationValueCase(BaseUseCase[list[ModificationValueWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех значений модификаций.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.
        - DTO `ModificationValueWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.

    Методы:
        execute(filter: ModificationValueFilter) -> list[ModificationValueWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех значений модификаций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationValueRepository(db)

    async def execute(self, filter: ModificationValueFilter) -> list[ModificationValueWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех значений модификаций.

        Args:
            filter (ModificationValueFilter): Фильтр для поиска и сортировки значений модификаций.

        Returns:
            list[ModificationValueWithRelationsRDTO]: Список объектов значений модификаций с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ModificationValueWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """