from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import FieldEntity


class FieldRepository(BaseRepository[FieldEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(FieldEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.image),
            selectinload(self.model.city),
            selectinload(self.model.field_parties),
        ]
