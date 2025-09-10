from typing import List, Optional

from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class TicketonBookingRequestDTO(BaseModel):
    seats: DTOConstant.StandardStringArrayField(description="Места")
    lang: DTOConstant.StandardVarcharField()
    show: DTOConstant.StandardVarcharField()
    email:DTOConstant.StandardEmailField()
    phone:DTOConstant.StandardVarcharField()


class TicketonBookingBonusDTO(BaseModel):
    """DTO для бонуса"""
    service: int
    amount: int


class TicketonBookingOrderTypeDTO(BaseModel):
    """DTO для типа оплаты заказа"""
    type: str
    label: str
    final: int
    hasStatusChecking: bool = False
    hasPaymentBySavedCard: bool = False
    hasOtpVerification: bool = False
    discount: int = 0
    isNewPage: bool = False

class TicketonBookingAdvertisingCampaignDTO(BaseModel):
    """DTO для рекламной кампании"""
    advertising_campaign_uid: Optional[int] = None
    active: Optional[int] = None
    name: Optional[str] = None
    page_text: Optional[str] = None
    image: Optional[str] = None


class TicketonBookingTicketDTO(BaseModel):
    id: Optional[str] = None
    level: Optional[str] = None
    row: Optional[str] = None
    num: Optional[str] = None
    cost: Optional[str] = None
    com: Optional[str] = None
    code: Optional[str] = None

class TicketonBookingShowBookingDTO(BaseModel):
    """DTO для ответа API бронирования шоу Ticketon"""

    show: str
    seats: List[str]
    lang: str
    freedom: bool = False
    sale: str
    reservation_id: str
    price: int
    sum: int
    expire: int
    currency: str
    hide_mfo: bool = False
    advertising_campaigns: Optional[List[TicketonBookingAdvertisingCampaignDTO]] = None
    special_bonus: Optional[List[TicketonBookingBonusDTO]] = None
    seats_text: Optional[List[str]] = None
    tickets: List[TicketonBookingTicketDTO]
    order: Optional[str] = None
    subscript: Optional[str] = None
    bonuses: Optional[dict[str, TicketonBookingBonusDTO]] = None
    order_types: Optional[List[TicketonBookingOrderTypeDTO]] = None
    sale_secury_token: str

    class Config:
        from_attributes = True


class TicketonBookingErrorResponseDTO(BaseModel):
    """DTO для ответа с ошибкой от Ticketon API"""
    status: int
    error: str