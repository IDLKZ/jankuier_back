from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import (
    AcademyGroupWithRelationsRDTO,
)
from app.adapters.filter.base_filter import BaseFilter
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.use_case.base_case import BaseUseCase


class AllAcademyGroupsCase(BaseUseCase[list[AcademyGroupWithRelationsRDTO]]):
    """
    Класс Use Case для получения всех групп академий с фильтрацией.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `AcademyGroupWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.

    Методы:
        execute(filter: BaseFilter) -> list[AcademyGroupWithRelationsRDTO]:
            Выполняет запрос и возвращает список групп академий.
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
        self.repository = AcademyGroupRepository(db)

    async def execute(self, filter: BaseFilter) -> list[AcademyGroupWithRelationsRDTO]:
        """
        Выполняет операцию получения всех групп академий с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[AcademyGroupWithRelationsRDTO]: Список групп академий с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            filters.append(
                or_(
                    func.lower(self.repository.model.name).like(search_term),
                    func.lower(self.repository.model.description_ru).like(search_term),
                    func.lower(self.repository.model.description_kk).like(search_term),
                    func.lower(self.repository.model.description_en).like(search_term),
                    func.lower(self.repository.model.value).like(search_term),
                )
            )

        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, "order_by", "id"),
            order_direction=getattr(filter, "order_direction", "asc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return [AcademyGroupWithRelationsRDTO.from_orm(model) for model in models]

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
