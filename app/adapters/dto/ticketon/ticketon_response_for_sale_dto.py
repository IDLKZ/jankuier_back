from pydantic import BaseModel
from typing import Dict, Any

from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingShowBookingDTO


class TicketonResponseForSaleDTO(BaseModel):
    order: Dict[str, Any] | None = None
    ticketon: TicketonBookingShowBookingDTO | None = None
    payment_transaction_id: int | None = None
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True