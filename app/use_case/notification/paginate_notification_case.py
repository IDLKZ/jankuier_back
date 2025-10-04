from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationNotificationWithRelationsRDTO
from app.adapters.filters.notification.notification_pagination_filter import (
    NotificationPaginationFilter,
)
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateNotificationCase(BaseUseCase[PaginationNotificationWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка уведомлений.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)

    async def execute(
        self, filter: NotificationPaginationFilter
    ) -> PaginationNotificationWithRelationsRDTO:
        models = await self.repository.paginate(
            dto=NotificationWithRelationsRDTO,
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
