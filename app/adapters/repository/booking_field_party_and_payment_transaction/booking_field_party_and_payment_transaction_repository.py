from typing import Any, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import \
    BookingFieldPartyAndPaymentTransactionCDTO
from app.adapters.repository.base_repository import BaseRepository
from app.entities import BookingFieldPartyAndPaymentTransactionEntity


class BookingFieldPartyAndPaymentTransactionRepository(BaseRepository[BookingFieldPartyAndPaymentTransactionEntity]):
    """
    Repository для работы со связями между бронированиями площадок и платежными транзакциями.

    Предоставляет специализированные методы для:
    - Управления связями между бронированиями и транзакциями
    - Поиска активных связей
    - Работы с основными транзакциями для бронирований
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(BookingFieldPartyAndPaymentTransactionEntity, db)

    def default_relationships(self) -> list[Any]:
        """Загружает связанные объекты по умолчанию"""
        return [
            selectinload(self.model.booking_request),
            selectinload(self.model.payment_transaction)
        ]

    async def get_active_links_for_request(
        self,
        request_id: int,
        include_deleted: bool = False
    ) -> List[BookingFieldPartyAndPaymentTransactionEntity]:
        """
        Получает все активные связи для бронирования.

        Args:
            request_id: ID бронирования площадки
            include_deleted: Включать удаленные записи

        Returns:
            Список активных связей
        """
        return await self.get_with_filters(
            filters=[
                self.model.request_id == request_id,
                self.model.is_active.is_(True)
            ],
            include_deleted_filter=include_deleted
        )

    async def get_active_links_for_transaction(
        self,
        payment_transaction_id: int,
        include_deleted: bool = False
    ) -> List[BookingFieldPartyAndPaymentTransactionEntity]:
        """
        Получает все активные связи для платежной транзакции.

        Args:
            payment_transaction_id: ID платежной транзакции
            include_deleted: Включать удаленные записи

        Returns:
            Список активных связей
        """
        return await self.get_with_filters(
            filters=[
                self.model.payment_transaction_id == payment_transaction_id,
                self.model.is_active.is_(True)
            ],
            include_deleted_filter=include_deleted
        )

    async def get_primary_transaction_for_request(
        self,
        request_id: int,
        include_deleted: bool = False
    ) -> Optional[BookingFieldPartyAndPaymentTransactionEntity]:
        """
        Получает основную транзакцию для бронирования.

        Args:
            request_id: ID бронирования площадки
            include_deleted: Включать удаленные записи

        Returns:
            Основная связь или None
        """
        return await self.get_first_with_filters(
            filters=[
                self.model.request_id == request_id,
                self.model.is_active.is_(True),
                self.model.is_primary.is_(True)
            ],
            include_deleted_filter=include_deleted
        )

    async def set_primary_transaction(
        self,
        request_id: int,
        payment_transaction_id: int
    ) -> BookingFieldPartyAndPaymentTransactionEntity:
        """
        Устанавливает указанную транзакцию как основную для бронирования.
        Сначала убирает флаг is_primary у всех других транзакций для этого бронирования.

        Args:
            request_id: ID бронирования площадки
            payment_transaction_id: ID платежной транзакции

        Returns:
            Обновленная связь

        Raises:
            ValueError: Если связь не найдена
        """
        # Убираем флаг is_primary у всех других связей для этого бронирования
        other_links = await self.get_with_filters(
            filters=[
                self.model.request_id == request_id,
                self.model.payment_transaction_id != payment_transaction_id,
                self.model.is_active.is_(True)
            ]
        )

        for link in other_links:
            link.is_primary = False
            await self.update(link, BookingFieldPartyAndPaymentTransactionCDTO.model_validate(link))

        # Находим и устанавливаем как основную нужную связь
        target_link = await self.get_first_with_filters(
            filters=[
                self.model.request_id == request_id,
                self.model.payment_transaction_id == payment_transaction_id,
                self.model.is_active.is_(True)
            ]
        )

        if not target_link:
            raise ValueError(
                f"Active link not found for request {request_id} and transaction {payment_transaction_id}"
            )

        target_link.is_primary = True
        return await self.update(target_link, BookingFieldPartyAndPaymentTransactionCDTO.model_validate(target_link))

    async def create_link(
        self,
        request_id: int,
        payment_transaction_id: int,
        link_type: str = "initial",
        link_reason: Optional[str] = None,
        is_primary: bool = False,
        is_active: bool = True
    ) -> BookingFieldPartyAndPaymentTransactionEntity:
        """
        Создает новую связь между бронированием и транзакцией.

        Args:
            request_id: ID бронирования площадки
            payment_transaction_id: ID платежной транзакции
            link_type: Тип связи (initial, recreated, refund, etc.)
            link_reason: Причина создания связи
            is_primary: Является ли основной
            is_active: Активна ли связь

        Returns:
            Созданная связь
        """
        entity = BookingFieldPartyAndPaymentTransactionEntity(
            request_id=request_id,
            payment_transaction_id=payment_transaction_id,
            link_type=link_type,
            link_reason=link_reason,
            is_primary=is_primary,
            is_active=is_active
        )

        return await self.create(entity)

    async def deactivate_links_for_request(
        self,
        request_id: int,
        exclude_transaction_id: Optional[int] = None
    ) -> int:
        """
        Деактивирует все связи для бронирования.

        Args:
            request_id: ID бронирования площадки
            exclude_transaction_id: ID транзакции, которую не нужно деактивировать

        Returns:
            Количество деактивированных связей
        """
        filters = [
            self.model.request_id == request_id,
            self.model.is_active.is_(True)
        ]

        if exclude_transaction_id:
            filters.append(self.model.payment_transaction_id != exclude_transaction_id)

        links = await self.get_with_filters(filters=filters)

        count = 0
        for link in links:
            link.is_active = False
            await self.update(link, BookingFieldPartyAndPaymentTransactionCDTO.model_validate(link))
            count += 1

        return count

    async def get_link_by_ids(
        self,
        request_id: int,
        payment_transaction_id: int,
        include_deleted: bool = False
    ) -> Optional[BookingFieldPartyAndPaymentTransactionEntity]:
        """
        Находит связь по ID бронирования и транзакции.

        Args:
            request_id: ID бронирования площадки
            payment_transaction_id: ID платежной транзакции
            include_deleted: Включать удаленные записи

        Returns:
            Найденная связь или None
        """
        return await self.get_first_with_filters(
            filters=[
                self.model.request_id == request_id,
                self.model.payment_transaction_id == payment_transaction_id
            ],
            include_deleted_filter=include_deleted
        )

    async def get_links_by_type(
        self,
        link_type: str,
        is_active: Optional[bool] = None,
        include_deleted: bool = False
    ) -> List[BookingFieldPartyAndPaymentTransactionEntity]:
        """
        Получает все связи определенного типа.

        Args:
            link_type: Тип связи
            is_active: Фильтр по активности
            include_deleted: Включать удаленные записи

        Returns:
            Список связей
        """
        filters = [self.model.link_type == link_type]

        if is_active is not None:
            filters.append(self.model.is_active.is_(is_active))

        return await self.get_with_filters(
            filters=filters,
            include_deleted_filter=include_deleted
        )