from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingShowBookingDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO


class AlatauHelper:
    @staticmethod
    def make_desc(dto: TicketonBookingShowBookingDTO,show:TicketonSingleShowResponseDTO|None) -> str:
        """
        Формирует строку DESC для платежной системы Alatau
        на основе брони из Ticketon.
        """
        ticket_places = []
        if dto.tickets:
            for t in dto.tickets:
                row = t.row or "?"
                num = t.num or "?"
                ticket_places.append(f"ряд {row}, место {num}")

        seats_desc = ", ".join(ticket_places) if ticket_places else "места не указаны"

        desc = (
            f"Оплата билетов: {show.event.name} , заказ {dto.sale}, "
            f"{seats_desc}, сумма {dto.sum} {dto.currency}, дата проведения {show.show.label}"
        )

        return desc

    @staticmethod
    def make_desc_from_ticketon_order(ticketon_order: TicketonOrderWithRelationsRDTO, show: TicketonSingleShowResponseDTO | None) -> str:
        """
        Формирует строку DESC для платежной системы Alatau
        на основе заказа Ticketon (TicketonOrderWithRelationsRDTO).
        """
        ticket_places = []
        if ticketon_order.tickets and isinstance(ticketon_order.tickets, list):
            for ticket in ticketon_order.tickets:
                if isinstance(ticket, dict):
                    row = ticket.get('row', '?')
                    num = ticket.get('num', '?')
                    ticket_places.append(f"ряд {row}, место {num}")

        seats_desc = ", ".join(ticket_places) if ticket_places else "места не указаны"

        event_name = "Мероприятие"
        show_date = "дата не указана"
        
        if show and show.event:
            event_name = show.event.name or event_name
        if show and show.show:
            show_date = show.show.label or show_date

        desc = (
            f"Оплата билетов: {event_name}, заказ {ticketon_order.sale}, "
            f"{seats_desc}, сумма {ticketon_order.sum} {ticketon_order.currency}, дата проведения {show_date}"
        )

        return desc