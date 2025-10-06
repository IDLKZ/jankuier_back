from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.repository.topic_notification.topic_notification_repository import (
    TopicNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TopicNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetTopicNotificationByIdCase(BaseUseCase[TopicNotificationWithRelationsRDTO]):
    """
    Use Case для получения топика уведомления по ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TopicNotificationRepository(db)
        self.model: TopicNotificationEntity | None = None

    async def execute(self, id: int) -> TopicNotificationWithRelationsRDTO:
        await self.validate(id=id)
        return TopicNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
