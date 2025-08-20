from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import UserVerificationEntity


class UserVerificationRepository(BaseRepository[UserVerificationEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(UserVerificationEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.user),
        ]
