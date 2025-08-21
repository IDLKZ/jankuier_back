from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import StudentEntity


class StudentRepository(BaseRepository[StudentEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(StudentEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.image),
            selectinload(self.model.created_by_user),
        ]
