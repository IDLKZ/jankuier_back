from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import AcademyGroupStudentEntity


class AcademyGroupStudentRepository(BaseRepository[AcademyGroupStudentEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(AcademyGroupStudentEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.student),
            selectinload(self.model.group),
            selectinload(self.model.request),
        ]