from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities.user_reset_password_code_entity import UserCodeResetPasswordEntity


class UserCodeResetPasswordRepository(BaseRepository[UserCodeResetPasswordEntity]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserCodeResetPasswordEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.user),
        ]
