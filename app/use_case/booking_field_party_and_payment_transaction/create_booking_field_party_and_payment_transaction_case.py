from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import (
    BookingFieldPartyAndPaymentTransactionCDTO,
    BookingFieldPartyAndPaymentTransactionWithRelationsRDTO
)
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import BookingFieldPartyAndPaymentTransactionRepository
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyAndPaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateBookingFieldPartyAndPaymentTransactionCase(BaseUseCase[BookingFieldPartyAndPaymentTransactionWithRelationsRDTO]):
    """
    Use Case для создания связи между бронированием площадки и платежной транзакцией.

    Используется для создания связей типа:
    - initial: Первоначальная оплата
    - recreated: Перевыставленный счет
    - refund: Возврат средств
    - И других типов связей

    Использует:
        - Repository `BookingFieldPartyAndPaymentTransactionRepository` для работы с базой данных
        - Repository `BookingFieldPartyRequestRepository` для валидации существования бронирования
        - Repository `PaymentTransactionRepository` для валидации существования транзакции
        - DTO `BookingFieldPartyAndPaymentTransactionCDTO` для входных данных
        - DTO `BookingFieldPartyAndPaymentTransactionWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyAndPaymentTransactionRepository): Репозиторий для работы со связями
        request_repository (BookingFieldPartyRequestRepository): Репозиторий для валидации бронирований
        transaction_repository (PaymentTransactionRepository): Репозиторий для валидации транзакций
        model (BookingFieldPartyAndPaymentTransactionEntity | None): Модель связи для создания

    Методы:
        execute(dto: BookingFieldPartyAndPaymentTransactionCDTO) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
            Создает новую связь и возвращает её с relationships
        validate(dto: BookingFieldPartyAndPaymentTransactionCDTO):
            Валидирует данные для создания связи
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyAndPaymentTransactionRepository(db)
        self.request_repository = BookingFieldPartyRequestRepository(db)
        self.transaction_repository = PaymentTransactionRepository(db)
        self.model: BookingFieldPartyAndPaymentTransactionEntity | None = None

    async def execute(self, dto: BookingFieldPartyAndPaymentTransactionCDTO) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию создания связи между бронированием и транзакцией.

        Args:
            dto (BookingFieldPartyAndPaymentTransactionCDTO): DTO с данными для создания связи

        Returns:
            BookingFieldPartyAndPaymentTransactionWithRelationsRDTO: Созданная связь с relationships

        Raises:
            AppExceptionResponse: При ошибках валидации (бронирование или транзакция не найдены, связь уже существует)
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return BookingFieldPartyAndPaymentTransactionWithRelationsRDTO.model_validate(model)

    async def validate(self, dto: BookingFieldPartyAndPaymentTransactionCDTO) -> None:
        """
        Валидация данных для создания связи между бронированием и транзакцией.

        Проверяет:
        - Существование бронирования (request_id)
        - Существование платежной транзакции (payment_transaction_id)
        - Отсутствие дублирующей связи между бронированием и транзакцией

        Args:
            dto (BookingFieldPartyAndPaymentTransactionCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если бронирование не найдено, транзакция не найдена или связь уже существует
        """
        # Проверяем существование бронирования
        request = await self.request_repository.get(dto.request_id)
        if not request:
            raise AppExceptionResponse.not_found(
                message=f"{i18n.gettext('booking_request_not_found')}: {dto.request_id}"
            )

        # Проверяем существование платежной транзакции
        transaction = await self.transaction_repository.get(dto.payment_transaction_id)
        if not transaction:
            raise AppExceptionResponse.not_found(
                message=f"{i18n.gettext('payment_transaction_not_found')}: {dto.payment_transaction_id}"
            )

        # Проверяем отсутствие дублирующей связи
        existing_link = await self.repository.get_link_by_ids(
            request_id=dto.request_id,
            payment_transaction_id=dto.payment_transaction_id,
            include_deleted=True
        )
        if existing_link:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("link_already_exists")
            )

        self.model = BookingFieldPartyAndPaymentTransactionEntity(**dto.model_dump())