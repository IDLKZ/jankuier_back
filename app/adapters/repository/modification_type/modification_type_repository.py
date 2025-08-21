from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ModificationTypeEntity


class ModificationTypeRepository(BaseRepository[ModificationTypeEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ModificationTypeEntity, db)

    def default_relationships(self) -> list[Any]:
        return []
