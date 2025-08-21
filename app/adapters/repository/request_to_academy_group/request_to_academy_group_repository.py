from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import RequestToAcademyGroupEntity


class RequestToAcademyGroupRepository(BaseRepository[RequestToAcademyGroupEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(RequestToAcademyGroupEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.student),
            selectinload(self.model.group),
            selectinload(self.model.checked_by_user),
        ]
