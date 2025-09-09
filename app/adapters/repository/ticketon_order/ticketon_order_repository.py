from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import TicketonOrderEntity


class TicketonOrderRepository(BaseRepository[TicketonOrderEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(TicketonOrderEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.status),
            selectinload(self.model.user),
            selectinload(self.model.payment_transaction)
        ]