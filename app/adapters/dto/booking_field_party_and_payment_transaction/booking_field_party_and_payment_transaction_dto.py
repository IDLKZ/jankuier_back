from pydantic import BaseModel
from typing import Optional

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import BookingFieldPartyRequestRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.shared.dto_constants import DTOConstant


class BookingFieldPartyAndPaymentTransactionDTO(BaseModel):
    """Базовый DTO для связи бронирования площадки и платежной транзакции"""
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class BookingFieldPartyAndPaymentTransactionCDTO(BaseModel):
    """
    DTO для создания связи между бронированием площадки и платежной транзакцией.

    Используется для:
    - Связывания нескольких попыток оплаты с одним бронированием (перевыставленные счета)
    - Связывания одной транзакции с несколькими бронированиями (групповая оплата)
    """

    request_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID бронирования площадки"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для бронирования"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи (initial, recreated, refund, etc.)"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )

    class Config:
        from_attributes = True


class BookingFieldPartyAndPaymentTransactionRDTO(BaseModel):
    """DTO для чтения связи между бронированием площадки и платежной транзакцией"""

    id: DTOConstant.StandardID()
    request_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID бронирования площадки"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для бронирования"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )
    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class BookingFieldPartyAndPaymentTransactionWithRelationsRDTO(BookingFieldPartyAndPaymentTransactionRDTO):
    """DTO для чтения связи с полными данными о бронировании и транзакции"""

    # Relationships
    booking_request: Optional[BookingFieldPartyRequestRDTO] = None
    payment_transaction: Optional[PaymentTransactionRDTO] = None

    class Config:
        from_attributes = True