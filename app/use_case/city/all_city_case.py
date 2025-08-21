from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.city.city_dto import CityWithRelationsRDTO
from app.adapters.filters.city.city_filter import CityFilter
from app.adapters.repository.city.city_repository import CityRepository
from app.use_case.base_case import BaseUseCase


class AllCityCase(BaseUseCase[list[CityWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех городов.

    Использует:
        - Репозиторий `CityRepository` для работы с базой данных.
        - DTO `CityWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CityRepository): Репозиторий для работы с городами.

    Методы:
        execute() -> list[CityWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех городов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CityRepository(db)

    async def execute(self, filter: CityFilter) -> list[CityWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех городов.

        Args:
            filter (CityFilter): Фильтр для поиска и сортировки.

        Returns:
            list[CityWithRelationsRDTO]: Список объектов городов с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [CityWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass