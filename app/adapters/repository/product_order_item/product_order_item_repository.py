from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductOrderItemEntity


class ProductOrderItemRepository(BaseRepository[ProductOrderItemEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductOrderItemEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.canceled_by),
            selectinload(self.model.status),
            selectinload(self.model.order),
            selectinload(self.model.from_city),
            selectinload(self.model.to_city),
            selectinload(self.model.variant),
            selectinload(self.model.product),
        ]