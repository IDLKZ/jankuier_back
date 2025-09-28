from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductOrderItemStatusEntity


class ProductOrderItemStatusRepository(BaseRepository[ProductOrderItemStatusEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductOrderItemStatusEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.previous_status),
            selectinload(self.model.next_status),
        ]