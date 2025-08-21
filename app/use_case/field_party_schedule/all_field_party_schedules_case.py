from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleWithRelationsRDTO,
)
from app.adapters.filters.field_party_schedule.field_party_schedule_filter import (
    FieldPartyScheduleFilter,
)
from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.use_case.base_case import BaseUseCase


class AllFieldPartySchedulesCase(
    BaseUseCase[list[FieldPartyScheduleWithRelationsRDTO]]
):
    """
    Класс Use Case для получения списка всех расписаний площадок.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.
        - DTO `FieldPartyScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями площадок.

    Методы:
        execute() -> list[FieldPartyScheduleWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех расписаний площадок.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleRepository(db)

    async def execute(
        self, filter: FieldPartyScheduleFilter
    ) -> list[FieldPartyScheduleWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех расписаний площадок.

        Args:
            filter (FieldPartyScheduleFilter): Фильтр для поиска и сортировки.

        Returns:
            list[FieldPartyScheduleWithRelationsRDTO]: Список объектов расписаний площадок с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [FieldPartyScheduleWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
