from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import AcademyGroupScheduleWithRelationsRDTO
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import AcademyGroupScheduleRepository
from app.use_case.base_case import BaseUseCase


class GetAcademyGroupScheduleByDayAndGroupUseCase(BaseUseCase[list[AcademyGroupScheduleWithRelationsRDTO]]):
    """
    Класс Use Case для получения расписания групп академии по дню и списку ID групп.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных расписания.
        - DTO `AcademyGroupScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписанием.

    Методы:
        execute(day: date, group_ids: list[int]) -> list[AcademyGroupScheduleWithRelationsRDTO]:
            Выполняет поиск расписания по дате и списку групп.
        validate(day: date, group_ids: list[int]):
            Проверяет входные данные.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupScheduleRepository(db)

    async def execute(self, day: date, group_ids: list[int]) -> list[AcademyGroupScheduleWithRelationsRDTO]:
        """
        Выполняет операцию получения расписания групп по дате и ID групп.

        Args:
            day (date): Дата тренировок в формате YYYY-MM-DD.
            group_ids (list[int]): Список ID групп академии.

        Returns:
            list[AcademyGroupScheduleWithRelationsRDTO]: Список расписаний с данными групп.
        """
        await self.validate(day=day, group_ids=group_ids)

        # Строим фильтры для поиска
        filters = [
            self.repository.model.training_date == day,
        ]
        
        # Добавляем фильтр по группам
        if len(group_ids) == 1:
            filters.append(self.repository.model.group_id == group_ids[0])
        else:
            filters.append(self.repository.model.group_id.in_(group_ids))

        # Получаем расписание с связанными данными
        schedules = await self.repository.get_all(
            filters=filters,
            options=self.repository.default_relationships(),
            include_deleted_filter=False,
            order_by="start_at"  # Сортируем по времени начала
        )

        # Конвертируем в DTO
        return [AcademyGroupScheduleWithRelationsRDTO.from_orm(schedule) for schedule in schedules]

    async def validate(self, day: date, group_ids: list[int]) -> None:
        """
        Валидация перед выполнением.

        Args:
            day (date): Дата для проверки.
            group_ids (list[int]): Список ID групп для проверки.

        Raises:
            ValueError: Если данные некорректны.
        """
        if not isinstance(day, date):
            raise ValueError("day must be a valid date")
            
        if not group_ids or not isinstance(group_ids, list):
            raise ValueError("group_ids must be a non-empty list")
            
        if not all(isinstance(group_id, int) and group_id > 0 for group_id in group_ids):
            raise ValueError("All group_ids must be positive integers")