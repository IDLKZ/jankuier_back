from typing import List

from pydantic import BaseModel

from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingTicketDTO
from app.shared.dto_constants import DTOConstant


class TicketonConfirmSaleRequestDTO(BaseModel):
    sale:DTOConstant.StandardVarcharField(description="Номер продажи")
    email:DTOConstant.StandardEmailField(description="Почта")
    phone:DTOConstant.StandardPhoneField(description="Номер телефона")


class TicketonConfirmSaleResponseDTO(BaseModel):
    status:DTOConstant.StandardIntegerField(description="1- успешно, 0 - ошибка")
    sale:DTOConstant.StandardNullableVarcharField(description="Код продажи")
    price:DTOConstant.StandardPriceField(description="Сумма покупки без верхней черты")
    expire:DTOConstant.StandardIntegerField(description="Время истечения в секундах")
    sum: DTOConstant.StandardPriceField(description="Сумма покупки c верхней черты")
    show: DTOConstant.StandardNullableVarcharField(description="Номер продажи")
    tickets: List[TicketonBookingTicketDTO]




