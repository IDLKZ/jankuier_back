from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_create_request_dto import \
    CreateBookingFieldPartyResponseDTO, CreateBookingFieldPartyRequestDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestCDTO,
    BookingFieldPartyRequestWithRelationsRDTO
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import \
    BookingFieldPartyAndPaymentTransactionRepository
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase
from app.use_case.field_party_schedule.preview_field_party_schedule_case import PreviewFieldPartyScheduleCase


class CreateClientBookingFieldRequestCase(BaseUseCase[CreateBookingFieldPartyResponseDTO]):


    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.booking_field_party_request_repository = BookingFieldPartyRequestRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.booking_field_party_and_payment_transaction_repository = BookingFieldPartyAndPaymentTransactionRepository(
            db)
        self.preview_field_party_schedule_case = PreviewFieldPartyScheduleCase(db)

        self.booking_field_entity: BookingFieldPartyRequestEntity | None = None


    async def execute(self, dto:CreateBookingFieldPartyRequestDTO, user:UserWithRelationsRDTO)->CreateBookingFieldPartyResponseDTO:
        pass



    async def validate(self):
        pass
