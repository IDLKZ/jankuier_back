from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyWithRelationsRDTO
from app.adapters.filters.academy.academy_filter import AcademyFilter
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.use_case.base_case import BaseUseCase


class AllAcademiesCase(BaseUseCase[list[AcademyWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех академий.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - DTO `AcademyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.

    Методы:
        execute() -> list[AcademyWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех академий.
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

    async def execute(self, filter: AcademyFilter) -> list[AcademyWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех академий.

        Args:
            filter (AcademyFilter): Фильтр для поиска и сортировки.

        Returns:
            list[AcademyWithRelationsRDTO]: Список объектов академий с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [AcademyWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
