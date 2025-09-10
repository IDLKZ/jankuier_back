from slugify import slugify

from app.shared.field_constants import FieldConstants


class DbValueConstants:
    # Роли
    AdminRoleConstantID = 1
    AdminRoleConstantValue = "system_admin"

    ClientRoleConstantID = 2
    ClientRoleConstantValue = "client"

    # Языки
    RussianLanguageConstantID = 1
    RussianLanguageConstantValue = "russian_language"
    KazakhLanguageConstantID = 2
    KazakhLanguageConstantValue = "kazakh_language"
    EnglishLanguageConstantID = 3
    EnglishLanguageConstantValue = "english_language"

    # Статусы заказов Ticketon
    TicketonOrderStatusBookingCreatedID = 1
    TicketonOrderStatusBookingCreatedValue = "booking_created_awaiting_payment"
    
    TicketonOrderStatusPaidConfirmedID = 2
    TicketonOrderStatusPaidConfirmedValue = "paid_and_confirmed"
    
    TicketonOrderStatusPaidAwaitingConfirmationID = 3
    TicketonOrderStatusPaidAwaitingConfirmationValue = "paid_awaiting_confirmation"
    
    TicketonOrderStatusCancelledID = 4
    TicketonOrderStatusCancelledValue = "cancelled"
    
    TicketonOrderStatusCancelledAwaitingRefundID = 5
    TicketonOrderStatusCancelledAwaitingRefundValue = "cancelled_awaiting_refund"
    
    TicketonOrderStatusCancelledRefundedID = 6
    TicketonOrderStatusCancelledRefundedValue = "cancelled_refunded"

    # Статусы платежных транзакций
    PaymentTransactionStatusAwaitingPaymentID = 1
    PaymentTransactionStatusAwaitingPaymentValue = "awaiting_payment"
    
    PaymentTransactionStatusPaidID = 2
    PaymentTransactionStatusPaidValue = "paid"
    
    PaymentTransactionStatusCancelledID = 3
    PaymentTransactionStatusCancelledValue = "cancelled"
    
    PaymentTransactionStatusFailedID = 4
    PaymentTransactionStatusFailedValue = "failed"
    
    PaymentTransactionStatusAwaitingRefundID = 5
    PaymentTransactionStatusAwaitingRefundValue = "awaiting_refund"
    
    PaymentTransactionStatusRefundedID = 6
    PaymentTransactionStatusRefundedValue = "refunded"

    PaymentTicketonType ="TICKETON_BOOKING"

    @staticmethod
    def get_value(title: str):
        return slugify(
            title,
            max_length=FieldConstants.STANDARD_VALUE_LENGTH,
            separator="_",
            lowercase=True,
        )
