from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.shared.dto_constants import DTOConstant


class TicketonOrderAndPaymentTransactionDTO(BaseModel):
    """Базовый DTO для связи заказа Ticketon и платежной транзакции"""
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionCDTO(BaseModel):
    """DTO для создания связи между заказом Ticketon и платежной транзакцией"""

    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи (initial, recreated, refund, etc.)"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionRDTO(BaseModel):
    """DTO для чтения связи между заказом Ticketon и платежной транзакцией"""

    id: DTOConstant.StandardID()
    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanFalseField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )
    created_at: DTOConstant.StandardDateTimeField(
        description="Дата создания"
    )
    updated_at: DTOConstant.StandardDateTimeField(
        description="Дата обновления"
    )
    deleted_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата удаления"
    )

    class Config:
        from_attributes = True


class TicketonOrderAndPaymentTransactionWithRelationsRDTO(BaseModel):
    """DTO для чтения связи с полными данными о заказе и транзакции"""

    id: DTOConstant.StandardID()
    ticketon_order_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID заказа Ticketon"
    )
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    is_active: DTOConstant.StandardBooleanFalseField(
        description="Активность связи"
    )
    is_primary: DTOConstant.StandardBooleanFalseField(
        description="Основная транзакция для заказа"
    )
    link_type: DTOConstant.StandardVarcharField(
        description="Тип связи"
    )
    link_reason: DTOConstant.StandardNullableTextField(
        description="Причина создания связи"
    )
    created_at: DTOConstant.StandardDateTimeField(
        description="Дата создания"
    )
    updated_at: DTOConstant.StandardDateTimeField(
        description="Дата обновления"
    )
    deleted_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата удаления"
    )

    # Relationships
    ticketon_order: Optional[TicketonOrderRDTO] = None
    payment_transaction: Optional[PaymentTransactionRDTO] = None

    class Config:
        from_attributes = True
