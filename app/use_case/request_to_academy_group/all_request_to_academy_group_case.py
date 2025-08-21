from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import RequestToAcademyGroupWithRelationsRDTO
from app.adapters.filters.request_to_academy_group.request_to_academy_group_filter import RequestToAcademyGroupFilter
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import RequestToAcademyGroupRepository
from app.use_case.base_case import BaseUseCase


class AllRequestToAcademyGroupCase(BaseUseCase[list[RequestToAcademyGroupWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех заявок в академические группы.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.
        - DTO `RequestToAcademyGroupWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.

    Методы:
        execute(filter: RequestToAcademyGroupFilter) -> list[RequestToAcademyGroupWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех заявок в академические группы.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RequestToAcademyGroupRepository(db)

    async def execute(self, filter: RequestToAcademyGroupFilter) -> list[RequestToAcademyGroupWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех заявок в академические группы.

        Args:
            filter (RequestToAcademyGroupFilter): Фильтр для поиска и сортировки заявок в академические группы.

        Returns:
            list[RequestToAcademyGroupWithRelationsRDTO]: Список объектов заявок в академические группы с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [RequestToAcademyGroupWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """