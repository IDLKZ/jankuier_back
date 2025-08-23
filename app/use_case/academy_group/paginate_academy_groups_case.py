from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationAcademyGroupWithRelationsRDTO
from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateAcademyGroupsCase(BaseUseCase[PaginationAcademyGroupWithRelationsRDTO]):
    """
    Класс Use Case для получения групп академий с пагинацией.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - Фильтр `PaginationFilter` для применения условий поиска, сортировки и пагинации.
        - DTO `PaginationAcademyGroupWithRelationsRDTO` для возврата данных с пагинацией.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.

    Методы:
        execute(filter: BasePaginationFilter) -> PaginationAcademyGroupWithRelationsRDTO:
            Выполняет запрос и возвращает группы академий с пагинацией.
        validate(filter: BasePaginationFilter):
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

    async def execute(
        self, filter: BasePaginationFilter
    ) -> PaginationAcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию получения групп академий с пагинацией.

        Args:
            filter (PaginationFilter): Объект фильтра с параметрами поиска, сортировки и пагинации.

        Returns:
            PaginationAcademyGroupWithRelationsRDTO: Пагинированный список групп академий с связями.
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

        # Получаем данные из репозитория с пагинацией
        result = await self.repository.paginate(
            dto=AcademyGroupWithRelationsRDTO,
            filters=filters,
            page=filter.page,
            per_page=filter.per_page,
            order_by=getattr(filter, "order_by", "id"),
            order_direction=getattr(filter, "order_direction", "asc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return result

    async def validate(self, filter: BasePaginationFilter) -> None:
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
