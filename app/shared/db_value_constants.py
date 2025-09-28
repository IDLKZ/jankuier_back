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
    ProductOrderType ="PRODUCT_ORDER"

    # Статусы заказов продуктов
    ProductOrderStatusCreatedAwaitingPaymentID = 1
    ProductOrderStatusCreatedAwaitingPaymentValue = "created_awaiting_payment"

    ProductOrderStatusPaidID = 2
    ProductOrderStatusPaidValue = "paid"

    ProductOrderStatusCancelledID = 3
    ProductOrderStatusCancelledValue = "cancelled"

    ProductOrderStatusCancelledAwaitingRefundID = 4
    ProductOrderStatusCancelledAwaitingRefundValue = "cancelled_awaiting_refund"

    ProductOrderStatusCancelledRefundedID = 5
    ProductOrderStatusCancelledRefundedValue = "cancelled_refunded"

    # Статусы элементов заказов продуктов
    ProductOrderItemStatusCreatedAwaitingPaymentID = 1
    ProductOrderItemStatusCreatedAwaitingPaymentValue = "created_awaiting_payment"

    ProductOrderItemStatusPaidAwaitingConfirmationID = 2
    ProductOrderItemStatusPaidAwaitingConfirmationValue = "paid_awaiting_confirmation"

    ProductOrderItemStatusInDeliveryID = 3
    ProductOrderItemStatusInDeliveryValue = "in_delivery"

    ProductOrderItemStatusAwaitingDeliveryConfirmationID = 4
    ProductOrderItemStatusAwaitingDeliveryConfirmationValue = "awaiting_delivery_confirmation"

    ProductOrderItemStatusSuccessfullyReceivedID = 5
    ProductOrderItemStatusSuccessfullyReceivedValue = "successfully_received"

    ProductOrderItemStatusCancelledID = 6
    ProductOrderItemStatusCancelledValue = "cancelled"

    ProductOrderItemStatusCancelledAwaitingRefundID = 7
    ProductOrderItemStatusCancelledAwaitingRefundValue = "cancelled_awaiting_refund"

    ProductOrderItemStatusCancelledRefundedID = 8
    ProductOrderItemStatusCancelledRefundedValue = "cancelled_refunded"

    @staticmethod
    def get_value(title: str):
        return slugify(
            title,
            max_length=FieldConstants.STANDARD_VALUE_LENGTH,
            separator="_",
            lowercase=True,
        )
