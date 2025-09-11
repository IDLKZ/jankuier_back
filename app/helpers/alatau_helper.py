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


from enum import Enum

class PaymentErrorCode(Enum):
    SERVICE_UNAVAILABLE = 11
    ORDER_INVALID = 12
    AMOUNT_INVALID = 13
    CURRENCY_INVALID = 14
    MPI_UNAVAILABLE = 15
    DB_UNAVAILABLE = 16
    MERCHANT_NOT_FOUND = 17
    MERCHANT_PROHIBITED = 171
    MERCHANT_AML_CFT = 172
    ORDER_ALREADY_IN_PROGRESS = 18
    CARD_EXP_DATE_INVALID = 19
    TERMINAL_INVALID = 20
    SIGNATURE_INVALID = 21
    CURRENCY_RATE_NOT_FOUND = 22
    LIMIT_EXCEEDED = 23
    FIELD_REQUIRED = 24
    FIELD_MIN_SIZE = 25
    FIELD_MAX_SIZE = 26
    FIELD_INVALID_VALUE = 27
    MPI_ERROR = 28
    INVALID_CARD_TYPE = 29
    INVOICE_NOT_FOUND = 30
    CLIENT_KEY_REQUIRED = 31
    TOKENIZATION_DISABLED = 32
    TOKEN_NOT_REGISTERED = 33
    BLOCK_AMOUNT_INVALID = 34
    UNKNOWN_ERROR = 99


ERROR_MESSAGES = {
    PaymentErrorCode.SERVICE_UNAVAILABLE: {
        "ru": "Сервис временно недоступен, попробуйте позже",
        "en": "Service temporary unavailable, try again later"
    },
    PaymentErrorCode.ORDER_INVALID: {
        "ru": "Неправильное значение в поле ORDER",
        "en": "Order number is invalid"
    },
    PaymentErrorCode.AMOUNT_INVALID: {
        "ru": "Неправильная сумма",
        "en": "Amount is invalid"
    },
    PaymentErrorCode.CURRENCY_INVALID: {
        "ru": "Неправильная валюта",
        "en": "Currency is invalid"
    },
    PaymentErrorCode.MPI_UNAVAILABLE: {
        "ru": "Сервис MPI временно недоступен, попробуйте позже",
        "en": "MPI service temporary unavailable, try again later"
    },
    PaymentErrorCode.DB_UNAVAILABLE: {
        "ru": "Сервис Db временно недоступен, попробуйте позже",
        "en": "Db service temporary unavailable, try again later"
    },
    PaymentErrorCode.MERCHANT_NOT_FOUND: {
        "ru": "Коммерсант не найден",
        "en": "Merchant not found"
    },
    PaymentErrorCode.MERCHANT_PROHIBITED: {
        "ru": "Коммерсанту запрещено выполнение операций",
        "en": "Merchant is prohibited from performing operations"
    },
    PaymentErrorCode.MERCHANT_AML_CFT: {
        "ru": "Коммерсанту запрещено проведение операций (Закон о ПОД/ФТ)",
        "en": "Merchant is prohibited from transactions in accordance with the AML/CFT Law"
    },
    PaymentErrorCode.ORDER_ALREADY_IN_PROGRESS: {
        "ru": "Запрос уже выполнялся",
        "en": "Request is already in progress"
    },
    PaymentErrorCode.CARD_EXP_DATE_INVALID: {
        "ru": "Неправильная дата действия карты (MM/ГГ)",
        "en": "Card exp date (MM/YY) is invalid"
    },
    PaymentErrorCode.TERMINAL_INVALID: {
        "ru": "Неправильное значение в поле TERMINAL",
        "en": "Terminal is invalid"
    },
    PaymentErrorCode.SIGNATURE_INVALID: {
        "ru": "Неправильная подпись!",
        "en": "Signature is invalid!"
    },
    PaymentErrorCode.CURRENCY_RATE_NOT_FOUND: {
        "ru": "Не найден курс валюты",
        "en": "The rate of currency is not found"
    },
    PaymentErrorCode.LIMIT_EXCEEDED: {
        "ru": "Превышен лимит!",
        "en": "Limit exceeded!"
    },
    PaymentErrorCode.FIELD_REQUIRED: {
        "ru": "Не указано значение в поле",
        "en": "The value of field is required"
    },
    PaymentErrorCode.FIELD_MIN_SIZE: {
        "ru": "Размер значения в поле менее допустимого",
        "en": "The size of value of the field is less than allowed"
    },
    PaymentErrorCode.FIELD_MAX_SIZE: {
        "ru": "Размер значения в поле больше допустимого",
        "en": "The size of value of the field is more than allowed"
    },
    PaymentErrorCode.FIELD_INVALID_VALUE: {
        "ru": "Введите валидное значение в поле",
        "en": "Enter a valid value of field"
    },
    PaymentErrorCode.MPI_ERROR: {
        "ru": "Ошибка MPI при выполнении проверки 3DS",
        "en": "MPI returns error during 3DS check"
    },
    PaymentErrorCode.INVALID_CARD_TYPE: {
        "ru": "Недопустимый тип карты",
        "en": "Invalid card type"
    },
    PaymentErrorCode.INVOICE_NOT_FOUND: {
        "ru": "Счёт на оплату не найден",
        "en": "Invoice is not found"
    },
    PaymentErrorCode.CLIENT_KEY_REQUIRED: {
        "ru": "Не передан ключ указанного клиента",
        "en": "The key of client is required"
    },
    PaymentErrorCode.TOKENIZATION_DISABLED: {
        "ru": "Для терминала запрещена токенизация",
        "en": "Card tokenisation disabled for terminal"
    },
    PaymentErrorCode.TOKEN_NOT_REGISTERED: {
        "ru": "Для данного клиента не зарегистрирован токен",
        "en": "Token is not registered for client of merchant"
    },
    PaymentErrorCode.BLOCK_AMOUNT_INVALID: {
        "ru": "Неверная сумма блокирования, заявка отменена!",
        "en": "Invalid blocking amount, order is cancelled!"
    },
    PaymentErrorCode.UNKNOWN_ERROR: {
        "ru": "Неизвестная ошибка",
        "en": "Unknown error"
    },
}


def get_alatau_error_message(code: int, lang: str = "ru") -> str:
    try:
        code_enum = PaymentErrorCode(code)
    except ValueError:
        return f"Неизвестный код ошибки: {code}"

    return ERROR_MESSAGES.get(code_enum, {}).get(lang, f"Нет описания для кода {code}")
