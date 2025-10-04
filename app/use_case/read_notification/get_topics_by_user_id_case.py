from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.topic_notification.topic_notification_dto import (
    TopicNotificationWithRelationsRDTO,
)
from app.adapters.repository.read_notification.read_notification_repository import (
    ReadNotificationRepository,
)
from app.entities import (
    ReadNotificationEntity,
    NotificationEntity,
    TopicNotificationEntity,
)
from app.use_case.base_case import BaseUseCase


class GetTopicsByUserIdCase(BaseUseCase[list[TopicNotificationWithRelationsRDTO]]):
    """
    Use Case для получения списка топиков уведомлений,
    которые прочитал пользователь.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = ReadNotificationRepository(db)
        self.db = db

    async def execute(self, user_id: int) -> list[TopicNotificationWithRelationsRDTO]:
        await self.validate(user_id=user_id)

        # Получаем уникальные топики из прочитанных уведомлений пользователя
        stmt = (
            select(TopicNotificationEntity)
            .join(
                NotificationEntity,
                NotificationEntity.topic_id == TopicNotificationEntity.id,
            )
            .join(
                ReadNotificationEntity,
                ReadNotificationEntity.notification_id == NotificationEntity.id,
            )
            .where(ReadNotificationEntity.user_id == user_id)
            .distinct()
            .options(selectinload(TopicNotificationEntity.image))
        )

        result = await self.db.execute(stmt)
        topics = result.scalars().unique().all()

        return [TopicNotificationWithRelationsRDTO.from_orm(topic) for topic in topics]

    async def validate(self, user_id: int) -> None:
        # Валидация user_id может быть добавлена здесь при необходимости
        pass
