from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationAcademyWithRelationsRDTO
from app.adapters.filters.academy.academy_pagination_filter import (
    AcademyPaginationFilter,
)
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.use_case.base_case import BaseUseCase


class PaginateAcademiesCase(BaseUseCase[PaginationAcademyWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка академий.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - DTO `PaginationAcademyWithRelationsRDTO` для возврата пагинированных данных с связями.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.

    Методы:
        execute() -> PaginationAcademyWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список академий.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyRepository(db)

    async def execute(
        self, filter: AcademyPaginationFilter
    ) -> PaginationAcademyWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка академий.

        Args:
            filter (AcademyPaginationFilter): Фильтр для поиска, сортировки и пагинации.

        Returns:
            PaginationAcademyWithRelationsRDTO: Пагинированный список академий с связями.
        """
        pagination_result = await self.repository.paginate(
            dto=AcademyWithRelationsRDTO,
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
