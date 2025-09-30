from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_dto import (
    BookingFieldPartyAndPaymentTransactionCDTO,
    BookingFieldPartyAndPaymentTransactionWithRelationsRDTO
)
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import BookingFieldPartyAndPaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyAndPaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateBookingFieldPartyAndPaymentTransactionCase(BaseUseCase[BookingFieldPartyAndPaymentTransactionWithRelationsRDTO]):
    """
    Use Case для обновления связи между бронированием площадки и платежной транзакцией.

    Используется для обновления параметров связи:
    - Изменение статуса активности (is_active)
    - Изменение флага основной транзакции (is_primary)
    - Изменение типа связи (link_type)
    - Изменение причины связи (link_reason)

    Использует:
        - Repository `BookingFieldPartyAndPaymentTransactionRepository` для работы с базой данных
        - DTO `BookingFieldPartyAndPaymentTransactionCDTO` для входных данных
        - DTO `BookingFieldPartyAndPaymentTransactionWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyAndPaymentTransactionRepository): Репозиторий для работы со связями
        model (BookingFieldPartyAndPaymentTransactionEntity | None): Модель связи для обновления

    Методы:
        execute(id: int, dto: BookingFieldPartyAndPaymentTransactionCDTO) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
            Обновляет связь и возвращает её с relationships
        validate(id: int, dto: BookingFieldPartyAndPaymentTransactionCDTO):
            Валидирует существование связи
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyAndPaymentTransactionRepository(db)
        self.model: BookingFieldPartyAndPaymentTransactionEntity | None = None

    async def execute(self, id: int, dto: BookingFieldPartyAndPaymentTransactionCDTO) -> BookingFieldPartyAndPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию обновления связи между бронированием и транзакцией.

        Args:
            id (int): ID связи для обновления
            dto (BookingFieldPartyAndPaymentTransactionCDTO): DTO с обновленными данными

        Returns:
            BookingFieldPartyAndPaymentTransactionWithRelationsRDTO: Обновленная связь с relationships

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return BookingFieldPartyAndPaymentTransactionWithRelationsRDTO.model_validate(model)

    async def validate(self, id: int, dto: BookingFieldPartyAndPaymentTransactionCDTO) -> None:
        """
        Валидация данных для обновления связи между бронированием и транзакцией.

        Проверяет существование связи.

        Args:
            id (int): ID связи для валидации
            dto (BookingFieldPartyAndPaymentTransactionCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        # Проверяем существование связи
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))