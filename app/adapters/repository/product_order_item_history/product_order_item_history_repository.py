from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductOrderItemHistoryEntity


class ProductOrderItemHistoryRepository(BaseRepository[ProductOrderItemHistoryEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductOrderItemHistoryEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.status),
            selectinload(self.model.responsible_user),
            selectinload(self.model.order_item),
        ]