from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.base_repository import BaseRepository
from app.entities import SportEntity


class SportRepository(BaseRepository[SportEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(SportEntity, db)

    def default_relationships(self) -> list[Any]:
        return []
