from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductOrderAndPaymentTransactionEntity


class ProductOrderAndPaymentTransactionRepository(BaseRepository[ProductOrderAndPaymentTransactionEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductOrderAndPaymentTransactionEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.payment_transaction),
            selectinload(self.model.product_order),
        ]