from typing import Optional, List
from pydantic import BaseModel

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.dto.product_order_status.product_order_status_dto import ProductOrderStatusRDTO
from app.adapters.dto.user.user_dto import UserRDTO
from app.shared.dto_constants import DTOConstant

class ProductOrderDTO(BaseModel):
    id: DTOConstant.StandardID("ID заказа")

    class Config:
        from_attributes = True


class ProductOrderCDTO(BaseModel):
    user_id: DTOConstant.StandardUnsignedIntegerField("ID пользователя")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса заказа")
    canceled_by_id: DTOConstant.StandardNullableUnsignedIntegerField("ID отменившего пользователя")
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField("ID платежной транзакции")

    shipping_total_price: DTOConstant.StandardZeroDecimalField("Стоимость доставки")
    taxes_price: DTOConstant.StandardZeroDecimalField("Налоги")
    total_price: DTOConstant.StandardPriceField("Общая стоимость")
    refunded_total: DTOConstant.StandardZeroDecimalField("Сумма возврата")

    order_items_snapshot: DTOConstant.StandardJSONField("Снапшот товаров")

    is_active: DTOConstant.StandardBooleanTrueField("Активен")
    is_canceled: DTOConstant.StandardBooleanFalseField("Отменён")
    is_paid: DTOConstant.StandardBooleanFalseField("Оплачен")
    is_refunded: DTOConstant.StandardBooleanFalseField("Возвращён")

    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")
    cancel_refund_reason: DTOConstant.StandardNullableTextField("Причина возврата")
    email: DTOConstant.StandardNullableVarcharField("Email")
    phone: DTOConstant.StandardNullableVarcharField("Телефон")
    paid_until: DTOConstant.StandardNullableDateTimeField("Срок оплаты")
    paid_at: DTOConstant.StandardNullableDateTimeField("Дата оплаты")
    paid_order: DTOConstant.StandardNullableVarcharField("Оплаченный заказ")

    class Config:
        from_attributes = True


class ProductOrderRDTO(ProductOrderDTO):
    user_id: DTOConstant.StandardUnsignedIntegerField("ID пользователя")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса заказа")
    canceled_by_id: DTOConstant.StandardNullableUnsignedIntegerField("ID отменившего пользователя")
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField("ID платежной транзакции")

    shipping_total_price: DTOConstant.StandardZeroDecimalField("Стоимость доставки")
    taxes_price: DTOConstant.StandardZeroDecimalField("Налоги")
    total_price: DTOConstant.StandardPriceField("Общая стоимость")
    refunded_total: DTOConstant.StandardZeroDecimalField("Сумма возврата")

    order_items_snapshot: DTOConstant.StandardJSONField("Снапшот товаров")

    is_active: DTOConstant.StandardBooleanTrueField("Активен")
    is_canceled: DTOConstant.StandardBooleanFalseField("Отменён")
    is_paid: DTOConstant.StandardBooleanFalseField("Оплачен")
    is_refunded: DTOConstant.StandardBooleanFalseField("Возвращён")

    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")
    cancel_refund_reason: DTOConstant.StandardNullableTextField("Причина возврата")
    email: DTOConstant.StandardNullableVarcharField("Email")
    phone: DTOConstant.StandardNullableVarcharField("Телефон")
    paid_until: DTOConstant.StandardNullableDateTimeField("Срок оплаты")
    paid_at: DTOConstant.StandardNullableDateTimeField("Дата оплаты")
    paid_order: DTOConstant.StandardNullableVarcharField("Оплаченный заказ")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductOrderWithRelationsRDTO(ProductOrderRDTO):
    user: Optional[UserRDTO] = None
    canceled_by: Optional[UserRDTO] = None
    status: Optional[ProductOrderStatusRDTO] = None
    payment_transaction: Optional[PaymentTransactionRDTO] = None

    class Config:
        from_attributes = True



