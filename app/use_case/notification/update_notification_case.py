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
from app.use_case.base_case import BaseUseCase


class UpdateNotificationCase(BaseUseCase[NotificationWithRelationsRDTO]):
    """
    Use Case для обновления уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.topic_repository = TopicNotificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model: NotificationEntity | None = None

    async def execute(
        self, id: int, dto: NotificationCDTO
    ) -> NotificationWithRelationsRDTO:
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return NotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: NotificationCDTO) -> None:
        # Проверка существования уведомления
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования топика
        topic = await self.topic_repository.get(dto.topic_id)
        if not topic:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("topic_not_found")
            )

        # Проверка существования пользователя (если указан)
        if dto.user_id is not None:
            user = await self.user_repository.get(dto.user_id)
            if not user:
                raise AppExceptionResponse.not_found(
                    message=i18n.gettext("user_not_found")
                )
