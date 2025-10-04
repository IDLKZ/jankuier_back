from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationFirebaseNotificationWithRelationsRDTO
from app.adapters.filters.firebase_notification.firebase_notification_pagination_filter import (
    FirebaseNotificationPaginationFilter,
)
from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateFirebaseNotificationCase(
    BaseUseCase[PaginationFirebaseNotificationWithRelationsRDTO]
):
    """
    Use Case для получения пагинированного списка Firebase уведомлений.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)

    async def execute(
        self, filter: FirebaseNotificationPaginationFilter
    ) -> PaginationFirebaseNotificationWithRelationsRDTO:
        models = await self.repository.paginate(
            dto=FirebaseNotificationWithRelationsRDTO,
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
