from pydantic import BaseModel
from datetime import datetime
from app.shared.dto_constants import DTOConstant

# Базовый DTO (только id)
class ProductOrderAndPaymentTransactionDTO(BaseModel):
    id: DTOConstant.StandardID("ID связи")

    class Config:
        from_attributes = True


# DTO для создания
class ProductOrderAndPaymentTransactionCDTO(BaseModel):
    product_order_id: DTOConstant.StandardUnsignedIntegerField("ID заказа")
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField("ID платежной транзакции")

    is_active: DTOConstant.StandardBooleanTrueField("Флаг активности")
    is_primary: DTOConstant.StandardBooleanFalseField("Основная транзакция для заказа")

    link_type: DTOConstant.StandardVarcharField("Тип связи ('initial', 'recreated', 'refund', etc.)")
    link_reason: DTOConstant.StandardNullableTextField("Причина создания связи")

    class Config:
        from_attributes = True


# DTO для чтения
class ProductOrderAndPaymentTransactionRDTO(ProductOrderAndPaymentTransactionDTO):
    product_order_id: DTOConstant.StandardUnsignedIntegerField("ID заказа")
    payment_transaction_id: DTOConstant.StandardUnsignedIntegerField("ID платежной транзакции")

    is_active: DTOConstant.StandardBooleanTrueField("Флаг активности")
    is_primary: DTOConstant.StandardBooleanFalseField("Основная транзакция для заказа")

    link_type: DTOConstant.StandardVarcharField("Тип связи ('initial', 'recreated', 'refund', etc.)")
    link_reason: DTOConstant.StandardNullableTextField("Причина создания связи")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


# DTO с отношениями
class ProductOrderAndPaymentTransactionWithRelationsRDTO(ProductOrderAndPaymentTransactionRDTO):
    product_order: "ProductOrderRDTO" | None = None
    payment_transaction: "PaymentTransactionRDTO" | None = None

    class Config:
        from_attributes = True
