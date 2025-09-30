from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import BookingFieldPartyStatusEntity


class BookingFieldPartyStatusRepository(BaseRepository[BookingFieldPartyStatusEntity]):
    """
    Repository для работы со статусами бронирования площадок (BookingFieldPartyStatus).

    Предоставляет методы для CRUD операций и работы с relationships:
    - previous_status: Предыдущий статус в цепочке
    - next_status: Следующий статус в цепочке
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(BookingFieldPartyStatusEntity, db)

    def default_relationships(self) -> list[Any]:
        """
        Загружает связанные статусы (previous_status, next_status).
        """
        return [
            selectinload(self.model.previous_status),
            selectinload(self.model.next_status)
        ]