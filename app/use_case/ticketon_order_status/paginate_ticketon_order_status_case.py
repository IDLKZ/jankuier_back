from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationTicketonOrderStatusWithRelationsRDTO
from app.adapters.filters.ticketon_order_status.ticketon_order_status_pagination_filter import TicketonOrderStatusPaginationFilter
from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusWithRelationsRDTO


class PaginateTicketonOrderStatusCase(BaseUseCase[PaginationTicketonOrderStatusWithRelationsRDTO]):
    """
    Класс Use Case для пагинации статусов заказов Ticketon.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.
        - DTO `TicketonOrderStatusWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationTicketonOrderStatusWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderStatusRepository(db)

    async def execute(
        self, filter: TicketonOrderStatusPaginationFilter
    ) -> PaginationTicketonOrderStatusWithRelationsRDTO:
        """
        Выполняет операцию пагинации статусов заказов Ticketon.

        Args:
            filter (TicketonOrderStatusPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationTicketonOrderStatusWithRelationsRDTO: Пагинированный результат со статусами.
        """
        models = await self.repository.paginate(
            dto=TicketonOrderStatusWithRelationsRDTO,
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