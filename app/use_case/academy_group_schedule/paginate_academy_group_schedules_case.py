from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import (
    AcademyGroupScheduleWithRelationsRDTO,
    PaginationAcademyGroupScheduleWithRelationsRDTO,
)
from app.adapters.filter.pagination_filter import PaginationFilter
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import (
    AcademyGroupScheduleRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateAcademyGroupSchedulesCase(
    BaseUseCase[PaginationAcademyGroupScheduleWithRelationsRDTO]
):
    """
    Класс Use Case для получения расписаний групп академий с пагинацией.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.
        - Фильтр `PaginationFilter` для применения условий поиска, сортировки и пагинации.
        - DTO `PaginationAcademyGroupScheduleWithRelationsRDTO` для возврата данных с пагинацией.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.

    Методы:
        execute(filter: PaginationFilter) -> PaginationAcademyGroupScheduleWithRelationsRDTO:
            Выполняет запрос и возвращает расписания с пагинацией.
        validate(filter: PaginationFilter):
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
        self.repository = AcademyGroupScheduleRepository(db)

    async def execute(
        self, filter: PaginationFilter
    ) -> PaginationAcademyGroupScheduleWithRelationsRDTO:
        """
        Выполняет операцию получения расписаний групп академий с пагинацией.

        Args:
            filter (PaginationFilter): Объект фильтра с параметрами поиска, сортировки и пагинации.

        Returns:
            PaginationAcademyGroupScheduleWithRelationsRDTO: Пагинированный список расписаний с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по полям связанной группы и дате/времени
            filters.append(
                or_(
                    func.lower(self.repository.model.group.name).like(search_term),
                    func.cast(
                        self.repository.model.training_date, func.text("TEXT")
                    ).like(search_term),
                    func.cast(self.repository.model.start_at, func.text("TEXT")).like(
                        search_term
                    ),
                    func.cast(self.repository.model.end_at, func.text("TEXT")).like(
                        search_term
                    ),
                )
            )

        # Получаем данные из репозитория с пагинацией
        result = await self.repository.paginate(
            dto=AcademyGroupScheduleWithRelationsRDTO,
            filters=filters,
            page=filter.page,
            per_page=filter.per_page,
            order_by=getattr(filter, "order_by", "training_date"),
            order_direction=getattr(filter, "order_direction", "asc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return result

    async def validate(self, filter: PaginationFilter) -> None:
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
