from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationCityWithRelationsRDTO
from app.adapters.dto.city.city_dto import CityWithRelationsRDTO
from app.adapters.filters.city.city_pagination_filter import CityPaginationFilter
from app.adapters.repository.city.city_repository import CityRepository
from app.use_case.base_case import BaseUseCase


class PaginateCityCase(BaseUseCase[PaginationCityWithRelationsRDTO]):
    """
    Класс Use Case для получения городов с пагинацией.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.
        - DTO `CityWithRelationsRDTO` для возврата данных с связями.
        - `PaginationCityWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.

    Методы:
        execute() -> PaginationCityWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список городов.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CityRepository(db)

    async def execute(
        self, filter: CityPaginationFilter
    ) -> PaginationCityWithRelationsRDTO:
        """
        Выполняет операцию получения городов с пагинацией.

        Args:
            filter (CityPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationCityWithRelationsRDTO: Пагинированный список городов с связями.
        """
        models = await self.repository.paginate(
            dto=CityWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
