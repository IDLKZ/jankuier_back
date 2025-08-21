from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party.field_party_dto import FieldPartyWithRelationsRDTO
from app.adapters.filters.field_party.field_party_filter import FieldPartyFilter
from app.adapters.repository.field_party.field_party_repository import FieldPartyRepository
from app.use_case.base_case import BaseUseCase


class AllFieldPartyCase(BaseUseCase[list[FieldPartyWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех площадок полей.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - DTO `FieldPartyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.

    Методы:
        execute() -> list[FieldPartyWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех площадок полей.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)

    async def execute(self, filter: FieldPartyFilter) -> list[FieldPartyWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех площадок полей.

        Args:
            filter (FieldPartyFilter): Фильтр для поиска и сортировки.

        Returns:
            list[FieldPartyWithRelationsRDTO]: Список объектов площадок полей с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [FieldPartyWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass