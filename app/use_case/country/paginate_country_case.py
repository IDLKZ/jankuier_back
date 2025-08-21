from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationCountryRDTO
from app.adapters.dto.country.country_dto import CountryRDTO
from app.adapters.filters.country.country_pagination_filter import (
    CountryPaginationFilter,
)
from app.adapters.repository.country.country_repository import CountryRepository
from app.use_case.base_case import BaseUseCase


class PaginateCountryCase(BaseUseCase[PaginationCountryRDTO]):
    """
    Класс Use Case для получения стран с пагинацией.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.
        - DTO `CountryRDTO` для возврата данных.
        - `PaginationCountryRDTO` для пагинированного ответа.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.

    Методы:
        execute() -> PaginationCountryRDTO:
            Выполняет запрос и возвращает пагинированный список стран.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)

    async def execute(self, filter: CountryPaginationFilter) -> PaginationCountryRDTO:
        """
        Выполняет операцию получения стран с пагинацией.

        Args:
            filter (CountryPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationCountryRDTO: Пагинированный список стран.
        """
        models = await self.repository.paginate(
            dto=CountryRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
