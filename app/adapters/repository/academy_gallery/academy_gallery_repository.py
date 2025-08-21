from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import AcademyGalleryEntity


class AcademyGalleryRepository(BaseRepository[AcademyGalleryEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(AcademyGalleryEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.academy),
            selectinload(self.model.group),
            selectinload(self.model.file),
        ]
