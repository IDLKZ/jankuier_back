from sqlalchemy import func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import (
    AcademyGroupScheduleWithRelationsRDTO,
)
from app.adapters.filter.base_filter import BaseFilter
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import (
    AcademyGroupScheduleRepository,
)
from app.use_case.base_case import BaseUseCase


class AllAcademyGroupSchedulesCase(
    BaseUseCase[list[AcademyGroupScheduleWithRelationsRDTO]]
):
    """
    Класс Use Case для получения всех расписаний групп академий с фильтрацией.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `AcademyGroupScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.

    Методы:
        execute(filter: BaseFilter) -> list[AcademyGroupScheduleWithRelationsRDTO]:
            Выполняет запрос и возвращает список расписаний групп академий.
        validate(filter: BaseFilter):
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
        self, filter: BaseFilter
    ) -> list[AcademyGroupScheduleWithRelationsRDTO]:
        """
        Выполняет операцию получения всех расписаний групп академий с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[AcademyGroupScheduleWithRelationsRDTO]: Список расписаний с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по полям связанной группы
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

        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, "order_by", "training_date"),
            order_direction=getattr(filter, "order_direction", "asc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return [
            AcademyGroupScheduleWithRelationsRDTO.from_orm(model) for model in models
        ]

    async def validate(self, filter: BaseFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (BaseFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
