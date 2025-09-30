from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import BookingFieldPartyAndPaymentTransactionWithRelationsRDTO
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import BookingFieldPartyAndPaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyAndPaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetBookingFieldPartyAndPaymentTransactionByIdCase(BaseUseCase[BookingFieldPartyAndPaymentTransactionWithRelationsRDTO]):
    """
    Use Case для получения связи между бронированием площадки и платежной транзакцией по ID.

    Используется для просмотра детальной информации о конкретной связи бронирования с транзакцией,
    включая тип связи (initial, recreated, refund), активность и основную транзакцию.

    Использует:
        - Repository `BookingFieldPartyAndPaymentTransactionRepository` для работы с базой данных
        - DTO `BookingFieldPartyAndPaymentTransactionWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyAndPaymentTransactionRepository): Репозиторий для работы со связями
        model (BookingFieldPartyAndPaymentTransactionEntity | None): Найденная модель связи

    Методы:
        execute(id: int) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
            Выполняет поиск связи по ID и возвращает её с relationships
        validate(id: int):
            Валидирует существование связи по ID
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyAndPaymentTransactionRepository(db)
        self.model: BookingFieldPartyAndPaymentTransactionEntity | None = None

    async def execute(self, id: int) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию получения связи между бронированием и транзакцией по ID.

        Args:
            id (int): ID связи для поиска

        Returns:
            BookingFieldPartyAndPaymentTransactionWithRelationsRDTO: Найденная связь с relationships (booking_request, payment_transaction)

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        await self.validate(id=id)
        return BookingFieldPartyAndPaymentTransactionWithRelationsRDTO.model_validate(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска связи между бронированием и транзакцией по ID.

        Args:
            id (int): ID связи для валидации

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))