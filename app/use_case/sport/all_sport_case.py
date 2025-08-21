from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sport.sport_dto import SportRDTO
from app.adapters.filters.sport.sport_filter import SportFilter
from app.adapters.repository.sport.sport_repository import SportRepository
from app.use_case.base_case import BaseUseCase


class AllSportCase(BaseUseCase[list[SportRDTO]]):
    """
    Класс Use Case для получения списка всех видов спорта.

    Использует:
        - Репозиторий `SportRepository` для работы с базой данных.
        - DTO `SportRDTO` для возврата данных.

    Атрибуты:
        repository (SportRepository): Репозиторий для работы с видами спорта.

    Методы:
        execute(filter: SportFilter) -> list[SportRDTO]:
            Выполняет запрос и возвращает список всех видов спорта.
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

    async def execute(self, filter: SportFilter) -> list[SportRDTO]:
        """
        Выполняет операцию получения списка всех видов спорта.

        Args:
            filter (SportFilter): Фильтр для поиска и сортировки видов спорта.

        Returns:
            list[SportRDTO]: Список объектов видов спорта.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [SportRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """