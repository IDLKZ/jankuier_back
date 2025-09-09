from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationTicketonOrderWithRelationsRDTO
from app.adapters.filters.ticketon_order.ticketon_order_pagination_filter import TicketonOrderPaginationFilter
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO


class PaginateTicketonOrderCase(BaseUseCase[PaginationTicketonOrderWithRelationsRDTO]):
    """
    Класс Use Case для пагинации заказов Ticketon.

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationTicketonOrderWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderRepository(db)

    async def execute(
        self, filter: TicketonOrderPaginationFilter
    ) -> PaginationTicketonOrderWithRelationsRDTO:
        """
        Выполняет операцию пагинации заказов Ticketon.

        Args:
            filter (TicketonOrderPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationTicketonOrderWithRelationsRDTO: Пагинированный результат с заказами.
        """
        models = await self.repository.paginate(
            dto=TicketonOrderWithRelationsRDTO,
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