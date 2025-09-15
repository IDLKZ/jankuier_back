from typing import List
from pydantic import BaseModel, Field

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.shared.dto_constants import DTOConstant


class TicketonTicketCheckSeatDTO(BaseModel):
    """DTO для информации о месте билета"""
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableVarcharField("ID места")
    row: DTOConstant.StandardNullableVarcharField("Номер ряда")
    num: DTOConstant.StandardNullableVarcharField("Номер места")


class TicketonTicketCheckItemDTO(BaseModel):
    """DTO для билета в ответе проверки билетов"""
    model_config = {"extra": "allow"}

    ticket: DTOConstant.StandardNullableVarcharField("Номер билета")
    seat: TicketonTicketCheckSeatDTO | None = Field(
        default=None,
        description="Информация о месте"
    )
    hall: DTOConstant.StandardNullableVarcharField("Зал")
    cost: DTOConstant.StandardNullableVarcharField("Стоимость билета")
    commission: DTOConstant.StandardNullableVarcharField("Комиссия")
    code: DTOConstant.StandardNullableVarcharField("Код билета")
    type: DTOConstant.StandardNullableVarcharField("Тип билета")
    barcode: DTOConstant.StandardNullableTextField("Штрих-код билета (Base64)")
    qr: DTOConstant.StandardNullableTextField("QR-код билета (Base64)")


class TicketonTicketCheckResponseDTO(BaseModel):
    """
    DTO для ответа API проверки билетов Ticketon
    Представляет список билетов с информацией о местах и кодами
    """
    model_config = {"extra": "allow"}

    tickets: List[TicketonTicketCheckItemDTO] = Field(
        description="Список билетов"
    )

    @classmethod
    def from_json(cls, data: List[dict]) -> "TicketonTicketCheckResponseDTO":
        """Создание DTO из JSON данных"""
        processed_tickets = []

        for ticket_data in data:
            processed_ticket = ticket_data.copy()

            # Обработка seat - преобразование в DTO объект
            if "seat" in processed_ticket and processed_ticket["seat"]:
                processed_ticket["seat"] = TicketonTicketCheckSeatDTO(**processed_ticket["seat"])

            processed_tickets.append(TicketonTicketCheckItemDTO(**processed_ticket))

        return cls(tickets=processed_tickets)


class TicketonTicketCheckCommonResponseDTO(BaseModel):
        ticketon_order: TicketonOrderWithRelationsRDTO | None = None
        ticket_check: TicketonTicketCheckResponseDTO | None = None
