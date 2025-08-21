from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field.field_dto import FieldWithRelationsRDTO
from app.adapters.filters.field.field_filter import FieldFilter
from app.adapters.repository.field.field_repository import FieldRepository
from app.use_case.base_case import BaseUseCase


class AllFieldCase(BaseUseCase[list[FieldWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех полей.

    Использует:
        - Репозиторий `FieldRepository` для работы с базой данных.
        - DTO `FieldWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldRepository): Репозиторий для работы с полями.

    Методы:
        execute() -> list[FieldWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех полей.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldRepository(db)

    async def execute(self, filter: FieldFilter) -> list[FieldWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех полей.

        Args:
            filter (FieldFilter): Фильтр для поиска и сортировки.

        Returns:
            list[FieldWithRelationsRDTO]: Список объектов полей с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [FieldWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
