from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationRequestToAcademyGroupWithRelationsRDTO
from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import RequestToAcademyGroupWithRelationsRDTO
from app.adapters.filters.request_to_academy_group.request_to_academy_group_pagination_filter import RequestToAcademyGroupPaginationFilter
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import RequestToAcademyGroupRepository
from app.use_case.base_case import BaseUseCase


class PaginateRequestToAcademyGroupCase(BaseUseCase[PaginationRequestToAcademyGroupWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка заявок в академические группы.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.
        - DTO `RequestToAcademyGroupWithRelationsRDTO` для возврата данных с отношениями.
        - Фильтр `RequestToAcademyGroupPaginationFilter` для пагинации и фильтрации.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.

    Методы:
        execute(filter: RequestToAcademyGroupPaginationFilter) -> PaginationRequestToAcademyGroupWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список заявок в академические группы.
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

    async def execute(self, filter: RequestToAcademyGroupPaginationFilter) -> PaginationRequestToAcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка заявок в академические группы.

        Args:
            filter (RequestToAcademyGroupPaginationFilter): Фильтр пагинации с параметрами поиска и сортировки.

        Returns:
            PaginationRequestToAcademyGroupWithRelationsRDTO: Объект пагинации с заявками в академические группы.
        """
        pagination = await self.repository.paginate(
            dto=RequestToAcademyGroupWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """