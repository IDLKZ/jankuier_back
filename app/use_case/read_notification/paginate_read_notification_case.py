from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationReadNotificationWithRelationsRDTO
from app.adapters.dto.read_notification.read_notification_dto import (
    ReadNotificationWithRelationsRDTO,
)
from app.adapters.filters.read_notification.read_notification_pagination_filter import (
    ReadNotificationPaginationFilter,
)
from app.adapters.repository.read_notification.read_notification_repository import (
    ReadNotificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateReadNotificationCase(
    BaseUseCase[PaginationReadNotificationWithRelationsRDTO]
):
    """
    Use Case для получения пагинированного списка прочитанных уведомлений.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = ReadNotificationRepository(db)

    async def execute(
        self, filter: ReadNotificationPaginationFilter
    ) -> PaginationReadNotificationWithRelationsRDTO:
        models = await self.repository.paginate(
            dto=ReadNotificationWithRelationsRDTO,
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
        pass
