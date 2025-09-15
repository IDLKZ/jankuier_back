from pydantic import BaseModel, Field

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.shared.dto_constants import DTOConstant


class TicketonTicketCheckSeatDTO(BaseModel):
    """DTO для информации о месте билета"""
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableVarcharField("ID места")
    row: DTOConstant.StandardNullableVarcharField("Номер ряда")
    num: DTOConstant.StandardNullableVarcharField("Номер места")


class TicketonTicketCheckResponseDTO(BaseModel):
    """
    DTO для ответа API проверки билета Ticketon
    Представляет один билет с информацией о месте и кодами
    """
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

    @classmethod
    def from_json(cls, data: dict) -> "TicketonTicketCheckResponseDTO":
        """Создание DTO из JSON данных"""
        # Проверяем структуру данных
        if not data or not isinstance(data, dict):
            return cls(
                ticket=None, seat=None, hall=None, cost=None,
                commission=None, code=None, type=None, barcode=None, qr=None
            )

        processed_data = data.copy()

        # Обработка seat - преобразование в DTO объект
        if "seat" in processed_data and processed_data["seat"]:
            processed_data["seat"] = TicketonTicketCheckSeatDTO(**processed_data["seat"])

        return cls(**processed_data)


class TicketonTicketCheckCommonResponseDTO(BaseModel):
        ticketon_order: TicketonOrderWithRelationsRDTO | None = None
        ticket_check: TicketonTicketCheckResponseDTO | None = None
