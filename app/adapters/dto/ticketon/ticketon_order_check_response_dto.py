from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.shared.dto_constants import DTOConstant


class TicketonOrderCheckTicketDTO(BaseModel):
    """DTO для билета в ответе проверки заказа"""
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableVarcharField("ID билета")
    seat_id: DTOConstant.StandardNullableVarcharField("ID места")
    row: DTOConstant.StandardNullableVarcharField("Ряд")
    number: DTOConstant.StandardNullableVarcharField("Номер места")
    level: DTOConstant.StandardNullableVarcharField("Сектор (или зал при отсутствии секторов)")
    hall_name: DTOConstant.StandardNullableVarcharField("Название зала")
    cost: DTOConstant.StandardNullableVarcharField("Стоимость")
    commission: DTOConstant.StandardNullableVarcharField("Комиссия по билету (в процентах)")
    type: DTOConstant.StandardNullableVarcharField("Тип билета")
    format: DTOConstant.StandardNullableVarcharField("Формат")
    code: DTOConstant.StandardNullableVarcharField("Код билета")
    place_code: DTOConstant.StandardNullableVarcharField("Код из внешней системы")
    reservation_code: DTOConstant.StandardNullableVarcharField("Код резервации заказа")
    sale_ticket_code: DTOConstant.StandardNullableVarcharField("Код билета из системы Тикетон")
    use_reserve_code: DTOConstant.StandardNullableIntegerField("Использовать код резерва для генерации QR")
    use_place_code: DTOConstant.StandardNullableIntegerField("Использовать place code для генерации QR")
    use_sale_place_code: DTOConstant.StandardNullableIntegerField("Использовать sale_ticket_code для генерации QR")
    use_ext_prefix: DTOConstant.StandardNullableIntegerField("Вставлять префикс EXT_ при генерации кода")
    barcode: DTOConstant.StandardNullableTextField("Штрих-код билета (Base64)")
    qr: DTOConstant.StandardNullableTextField("QR-код билета (Base64)")


class TicketonOrderCheckSaleDTO(BaseModel):
    """DTO для информации о продаже/заказе"""
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableVarcharField("ID заказа")
    sale_id: DTOConstant.StandardNullableVarcharField("Deprecated field")
    reservation_code: DTOConstant.StandardNullableVarcharField("Код резервации")
    date: DTOConstant.StandardNullableVarcharField("Дата создания заказа (YYYY-MM-DD HH:MM)")
    price: DTOConstant.StandardNullableIntegerField("Сумма заказа")
    final_price: DTOConstant.StandardNullableIntegerField("Цена с комиссией")
    status: DTOConstant.StandardNullableVarcharField("Статус заказа")
    expire: DTOConstant.StandardNullableVarcharField("Время истечения заказа (YYYY-MM-DD HH:MM)")
    commission: DTOConstant.StandardNullableIntegerField("Комиссия")


class TicketonOrderCheckShowDTO(BaseModel):
    """DTO для информации о событии"""
    model_config = {"extra": "allow"}

    id: DTOConstant.StandardNullableVarcharField("ID события")
    date: DTOConstant.StandardNullableVarcharField("Дата события (YYYY-MM-DD HH:MM)")
    description: DTOConstant.StandardNullableTextField("Описание события")
    information: DTOConstant.StandardNullableTextField("Дополнительная информация (HTML)")
    duration: DTOConstant.StandardNullableVarcharField("Длительность (минуты)")
    action: DTOConstant.StandardNullableVarcharField("Название события")
    place: DTOConstant.StandardNullableVarcharField("Место проведения")
    address: DTOConstant.StandardNullableVarcharField("Адрес проведения")
    hall: DTOConstant.StandardNullableVarcharField("Наименование зала")
    type: DTOConstant.StandardNullableVarcharField("Тип события")


class TicketonOrderCheckResponseDTO(BaseModel):
    """
    DTO для ответа API проверки заказа Ticketon
    Представляет один заказ с билетами, информацией о продаже и событии
    """
    model_config = {"extra": "allow"}

    tickets: Optional[Dict[str, TicketonOrderCheckTicketDTO]] = Field(
        default=None,
        description="Словарь билетов (ключ = ID билета)"
    )
    sale: Optional[TicketonOrderCheckSaleDTO] = Field(
        default=None,
        description="Информация о продаже/заказе"
    )
    show: Optional[TicketonOrderCheckShowDTO] = Field(
        default=None,
        description="Информация о событии"
    )

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "TicketonOrderCheckResponseDTO":
        """Создание DTO из JSON данных"""
        # Проверяем структуру данных
        if not data or not isinstance(data, dict):
            return cls(tickets=None, sale=None, show=None)

        # Обработка tickets - преобразование в DTO объекты
        tickets = None
        if "tickets" in data and data["tickets"]:
            tickets_dict = {}
            for ticket_id, ticket_data in data["tickets"].items():
                if isinstance(ticket_data, dict):
                    tickets_dict[str(ticket_id)] = TicketonOrderCheckTicketDTO(**ticket_data)
            tickets = tickets_dict if tickets_dict else None

        # Обработка sale
        sale = None
        if "sale" in data and data["sale"]:
            sale = TicketonOrderCheckSaleDTO(**data["sale"])

        # Обработка show
        show = None
        if "show" in data and data["show"]:
            show = TicketonOrderCheckShowDTO(**data["show"])

        return cls(tickets=tickets, sale=sale, show=show)


# Статусы заказов для справки
class TicketonOrderCheckStatus:
    """Константы статусов заказов Ticketon"""
    EXPIRING_NOT_CONFIRMED = "1"  # истекает, не подтверждён
    CONFIRMED = "2"              # подтверждён
    CANCELLED_EXPIRING = "3"     # отменён истекающий
    REFUND_CONFIRMED = "4"       # возврат подтверждённого


class TicketonOrderCheckCommonResponseDTO(BaseModel):
    ticketon_order:TicketonOrderWithRelationsRDTO|None = None
    order_check:TicketonOrderCheckResponseDTO|None = None
