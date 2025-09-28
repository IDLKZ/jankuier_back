from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductOrderEntity


class ProductOrderRepository(BaseRepository[ProductOrderEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductOrderEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.payment_transaction),
            selectinload(self.model.user),
            selectinload(self.model.canceled_by),
            selectinload(self.model.status),
            selectinload(self.model.order_items),
            selectinload(self.model.payment_transactions),
        ]