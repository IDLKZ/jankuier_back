from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationCDTO,
    NotificationWithRelationsRDTO,
)
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.adapters.repository.topic_notification.topic_notification_repository import (
    TopicNotificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import NotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.firebase_service.firebase_service import FireBaseService
from app.use_case.base_case import BaseUseCase


class CreateNotificationCase(BaseUseCase[NotificationWithRelationsRDTO]):
    """
    Use Case для создания уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.topic_repository = TopicNotificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model: NotificationEntity | None = None
        self.firebase_service = FireBaseService(db)

    async def execute(self, dto: NotificationCDTO) -> NotificationWithRelationsRDTO:
        await self.validate(dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return NotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: NotificationCDTO) -> None:
        # Проверка существования топика
        topic = await self.topic_repository.get(dto.topic_id)
        if not topic:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("topic_not_found")
            )

        # Проверка существования пользователя (если указан)
        if dto.user_id is not None:
            user = await self.user_repository.get(dto.user_id)
            if not user:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("user_not_found")
                )

        self.model = NotificationEntity(**dto.dict())
        await self.firebase_service.send_notifications_async(self.model)
