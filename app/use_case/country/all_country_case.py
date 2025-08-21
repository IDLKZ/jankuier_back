from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.country.country_dto import CountryRDTO
from app.adapters.filters.country.country_filter import CountryFilter
from app.adapters.repository.country.country_repository import CountryRepository
from app.use_case.base_case import BaseUseCase


class AllCountryCase(BaseUseCase[list[CountryRDTO]]):
    """
    Класс Use Case для получения списка всех стран.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.
        - DTO `CountryRDTO` для возврата данных.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.

    Методы:
        execute() -> list[CountryRDTO]:
            Выполняет запрос и возвращает список всех стран.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)

    async def execute(self, filter: CountryFilter) -> list[CountryRDTO]:
        """
        Выполняет операцию получения списка всех стран.

        Args:
            filter (CountryFilter): Фильтр для поиска и сортировки.

        Returns:
            list[CountryRDTO]: Список объектов стран.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [CountryRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
