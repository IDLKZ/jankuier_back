from sqlalchemy import and_
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


class UpdateTopicNotificationCase(BaseUseCase[TopicNotificationWithRelationsRDTO]):
    """
    Use Case для обновления топика уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TopicNotificationRepository(db)
        self.model: TopicNotificationEntity | None = None

    async def execute(
        self, id: int, dto: TopicNotificationCDTO
    ) -> TopicNotificationWithRelationsRDTO:
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return TopicNotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: TopicNotificationCDTO) -> None:
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.value == dto.value,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )
