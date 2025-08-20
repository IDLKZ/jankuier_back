from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ModificationValueEntity


class ModificationValueRepository(BaseRepository[ModificationValueEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ModificationValueEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.modification_type),
            selectinload(self.model.product),
        ]