from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import NotificationEntity, TopicNotificationEntity


class NotificationRepository(BaseRepository[NotificationEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(NotificationEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.topic).selectinload(
                TopicNotificationEntity.image
            ),
            selectinload(self.model.user),
            selectinload(self.model.read_notifications),
        ]
