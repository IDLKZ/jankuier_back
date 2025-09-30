from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import BookingFieldPartyRequestEntity


class BookingFieldPartyRequestRepository(BaseRepository[BookingFieldPartyRequestEntity]):
    """
    Repository для работы с бронированиями площадок (BookingFieldPartyRequest).

    Предоставляет методы для CRUD операций и работы с relationships:
    - status: Статус бронирования
    - user: Пользователь, создавший бронирование
    - field: Площадка (для индивидуального бронирования)
    - field_party: Групповое мероприятие (для группового бронирования)
    - payment_transaction: Основная платежная транзакция
    - payment_transactions: Все связанные платежные транзакции (через связующую таблицу)
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(BookingFieldPartyRequestEntity, db)

    def default_relationships(self) -> list[Any]:
        """
        Загружает основные relationships для бронирования.
        """
        return [
            selectinload(self.model.status),
            selectinload(self.model.user),
            selectinload(self.model.field),
            selectinload(self.model.field_party),
            selectinload(self.model.payment_transaction)
        ]