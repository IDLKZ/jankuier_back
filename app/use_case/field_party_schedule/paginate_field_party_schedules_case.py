from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import (
    PaginationFieldPartyScheduleWithRelationsRDTO,
)
from app.adapters.filters.field_party_schedule.field_party_schedule_pagination_filter import (
    FieldPartySchedulePaginationFilter,
)
from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateFieldPartySchedulesCase(
    BaseUseCase[PaginationFieldPartyScheduleWithRelationsRDTO]
):
    """
    Класс Use Case для получения пагинированного списка расписаний площадок.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.
        - DTO `PaginationFieldPartyScheduleWithRelationsRDTO` для возврата пагинированных данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями площадок.

    Методы:
        execute() -> PaginationFieldPartyScheduleWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список расписаний площадок.
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
        self, filter: FieldPartySchedulePaginationFilter
    ) -> PaginationFieldPartyScheduleWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка расписаний площадок.

        Args:
            filter (FieldPartySchedulePaginationFilter): Фильтр для поиска, сортировки и пагинации.

        Returns:
            PaginationFieldPartyScheduleWithRelationsRDTO: Пагинированный список расписаний площадок с связями.
        """
        pagination_result = await self.repository.paginate(
            dto=FieldPartyScheduleWithRelationsRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            page=filter.page,
            per_page=filter.per_page,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination_result

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
