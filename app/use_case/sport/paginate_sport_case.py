from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationSportRDTO
from app.adapters.dto.sport.sport_dto import SportRDTO
from app.adapters.filters.sport.sport_pagination_filter import SportPaginationFilter
from app.adapters.repository.sport.sport_repository import SportRepository
from app.use_case.base_case import BaseUseCase


class PaginateSportCase(BaseUseCase[PaginationSportRDTO]):
    """
    Класс Use Case для получения пагинированного списка видов спорта.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.
        - DTO `SportRDTO` для возврата данных.
        - Фильтр `SportPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.

    Методы:
        execute(filter: SportPaginationFilter) -> PaginationSportRDTO:
            Выполняет запрос и возвращает пагинированный список видов спорта.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = SportRepository(db)

    async def execute(self, filter: SportPaginationFilter) -> PaginationSportRDTO:
        """
        Выполняет операцию получения пагинированного списка видов спорта.

        Args:
            filter (SportPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationSportRDTO: Объект пагинации с видами спорта.
        """
        pagination = await self.repository.paginate(
            dto=SportRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """