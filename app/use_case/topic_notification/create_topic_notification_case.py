from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationCDTO,
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.repository.topic_notification.topic_notification_repository import (
    TopicNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TopicNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateTopicNotificationCase(BaseUseCase[TopicNotificationWithRelationsRDTO]):
    """
    Use Case для создания топика уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TopicNotificationRepository(db)
        self.model: TopicNotificationEntity | None = None

    async def execute(
        self, dto: TopicNotificationCDTO
    ) -> TopicNotificationWithRelationsRDTO:
        await self.validate(dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return TopicNotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: TopicNotificationCDTO) -> None:
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )

        self.model = TopicNotificationEntity(**dto.dict())
