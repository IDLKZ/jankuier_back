from pydantic import BaseModel

from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import \
    BookingFieldPartyRequestWithRelationsRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.shared.dto_constants import DTOConstant


class CreateBookingFieldPartyRequestDTO(BaseModel):
    field_party_id: DTOConstant.StandardIntegerField(
        description="ID группового мероприятия на площадке"
    )
    day: str
    start_at: str
    end_at: str


class CreateBookingFieldPartyResponseDTO:
    field_booking_request:BookingFieldPartyRequestWithRelationsRDTO|None = None
    payment_transaction:PaymentTransactionRDTO|None = None
    order:AlatauCreateResponseOrderDTO|None = None
    success:bool = False
    message:str = "Бронирование поля"

