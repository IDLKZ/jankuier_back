from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.filters.topic_notification.topic_notification_filter import (
    TopicNotificationFilter,
)
from app.adapters.repository.topic_notification.topic_notification_repository import (
    TopicNotificationRepository,
)
from app.use_case.base_case import BaseUseCase


class AllTopicNotificationCase(BaseUseCase[list[TopicNotificationWithRelationsRDTO]]):
    """
    Use Case для получения списка всех топиков уведомлений.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TopicNotificationRepository(db)

    async def execute(
        self, filter: TopicNotificationFilter
    ) -> list[TopicNotificationWithRelationsRDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
            options=self.repository.default_relationships(),
        )
        return [TopicNotificationWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        pass
