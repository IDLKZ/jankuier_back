from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import BookingFieldPartyAndPaymentTransactionWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO
from app.adapters.filters.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_pagination_filter import BookingFieldPartyAndPaymentTransactionPaginationFilter
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import BookingFieldPartyAndPaymentTransactionRepository
from app.use_case.base_case import BaseUseCase


class PaginateBookingFieldPartyAndPaymentTransactionCase(BaseUseCase[PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO]):
    """
    Use Case для пагинации связей между бронированиями площадок и платежными транзакциями.

    Использует:
        - Repository `BookingFieldPartyAndPaymentTransactionRepository` для работы с базой данных
        - DTO `BookingFieldPartyAndPaymentTransactionWithRelationsRDTO` для возврата данных с relationships
        - `PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO` для пагинированного ответа

    Атрибуты:
        repository (BookingFieldPartyAndPaymentTransactionRepository): Репозиторий для работы со связями

    Методы:
        execute(filter: BookingFieldPartyAndPaymentTransactionPaginationFilter) -> PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
            Выполняет пагинацию связей с фильтрацией
        validate():
            Валидация (не используется в данном случае)
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyAndPaymentTransactionRepository(db)

    async def execute(
        self, filter: BookingFieldPartyAndPaymentTransactionPaginationFilter
    ) -> PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию пагинации связей между бронированиями и транзакциями.

        Args:
            filter (BookingFieldPartyAndPaymentTransactionPaginationFilter): Фильтр с параметрами пагинации, поиска и сортировки

        Returns:
            PaginationBookingFieldPartyAndPaymentTransactionWithRelationsRDTO: Пагинированный результат со связями и relationships
        """
        models = await self.repository.paginate(
            dto=BookingFieldPartyAndPaymentTransactionWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (не используется).
        """
        pass