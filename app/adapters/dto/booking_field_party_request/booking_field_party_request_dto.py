from pydantic import BaseModel

from app.adapters.dto.booking_field_party_status.booking_field_party_status_dto import BookingFieldPartyStatusRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.field.field_dto import FieldRDTO
from app.adapters.dto.field_party.field_party_dto import FieldPartyRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.shared.dto_constants import DTOConstant


class BookingFieldPartyRequestDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class BookingFieldPartyRequestCDTO(BaseModel):
    """
    DTO для создания/обновления бронирования площадки.
    """
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID статуса бронирования"
    )
    user_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID пользователя"
    )
    field_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID площадки"
    )
    field_party_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID группового мероприятия на площадке"
    )
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    total_price: DTOConstant.StandardPriceField(
        description="Общая стоимость бронирования"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности"
    )
    is_canceled: DTOConstant.StandardBooleanFalseField(
        description="Флаг отмены"
    )
    is_paid: DTOConstant.StandardBooleanFalseField(
        description="Флаг оплаты"
    )
    is_refunded: DTOConstant.StandardBooleanFalseField(
        description="Флаг возврата средств"
    )
    cancel_reason: DTOConstant.StandardNullableTextField(
        description="Причина отмены"
    )
    cancel_refund_reason: DTOConstant.StandardNullableTextField(
        description="Причина возврата средств"
    )
    email: DTOConstant.StandardNullableVarcharField(
        description="Email для связи"
    )
    phone: DTOConstant.StandardNullableVarcharField(
        description="Телефон для связи"
    )
    paid_until: DTOConstant.StandardNullableDateTimeField(
        description="Оплачено до (срок действия)"
    )
    paid_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата и время оплаты"
    )
    paid_order: DTOConstant.StandardNullableVarcharField(
        description="Номер платежного заказа"
    )
    start_at: DTOConstant.StandardDateTimeField(
        description="Начало бронирования"
    )
    end_at: DTOConstant.StandardDateTimeField(
        description="Конец бронирования"
    )
    reschedule_start_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенное начало бронирования"
    )
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенный конец бронирования"
    )

    class Config:
        from_attributes = True


class BookingFieldPartyRequestRDTO(BookingFieldPartyRequestDTO):
    """
    DTO для чтения бронирования площадки.
    """
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID статуса бронирования"
    )
    user_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID пользователя"
    )
    field_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID площадки"
    )
    field_party_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID группового мероприятия на площадке"
    )
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    total_price: DTOConstant.StandardPriceField(
        description="Общая стоимость бронирования"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности"
    )
    is_canceled: DTOConstant.StandardBooleanFalseField(
        description="Флаг отмены"
    )
    is_paid: DTOConstant.StandardBooleanFalseField(
        description="Флаг оплаты"
    )
    is_refunded: DTOConstant.StandardBooleanFalseField(
        description="Флаг возврата средств"
    )
    cancel_reason: DTOConstant.StandardNullableTextField(
        description="Причина отмены"
    )
    cancel_refund_reason: DTOConstant.StandardNullableTextField(
        description="Причина возврата средств"
    )
    email: DTOConstant.StandardNullableVarcharField(
        description="Email для связи"
    )
    phone: DTOConstant.StandardNullableVarcharField(
        description="Телефон для связи"
    )
    paid_until: DTOConstant.StandardNullableDateTimeField(
        description="Оплачено до (срок действия)"
    )
    paid_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата и время оплаты"
    )
    paid_order: DTOConstant.StandardNullableVarcharField(
        description="Номер платежного заказа"
    )
    start_at: DTOConstant.StandardDateTimeField(
        description="Начало бронирования"
    )
    end_at: DTOConstant.StandardDateTimeField(
        description="Конец бронирования"
    )
    reschedule_start_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенное начало бронирования"
    )
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(
        description="Перенесенный конец бронирования"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class BookingFieldPartyRequestWithRelationsRDTO(BookingFieldPartyRequestRDTO):
    """
    DTO для чтения бронирования площадки с relationships.
    """
    status: BookingFieldPartyStatusRDTO | None = None
    user: UserRDTO | None = None
    field: FieldRDTO | None = None
    field_party: FieldPartyRDTO | None = None
    payment_transaction: PaymentTransactionRDTO | None = None

    class Config:
        from_attributes = True