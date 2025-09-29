from typing import Optional, List
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant

class ProductOrderItemDTO(BaseModel):
    id: DTOConstant.StandardID("ID элемента заказа")

    class Config:
        from_attributes = True


class ProductOrderItemCDTO(BaseModel):
    order_id: DTOConstant.StandardUnsignedIntegerField("ID заказа")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса позиции")
    canceled_by_id: DTOConstant.StandardNullableUnsignedIntegerField("ID отменившего пользователя")
    product_id: DTOConstant.StandardUnsignedIntegerField("ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField("ID варианта")
    from_city_id: DTOConstant.StandardNullableUnsignedIntegerField("ID города отправления")
    to_city_id: DTOConstant.StandardNullableUnsignedIntegerField("ID города прибытия")

    qty: DTOConstant.StandardIntegerField("Количество")
    sku: DTOConstant.StandardNullableVarcharField("SKU товара")
    product_price: DTOConstant.StandardPriceField("Цена продукта")
    delta_price: DTOConstant.StandardZeroDecimalField("Изменение цены")
    shipping_price: DTOConstant.StandardZeroDecimalField("Стоимость доставки")

    refunded_total: DTOConstant.StandardZeroDecimalField("Возвращённая сумма")
    is_active: DTOConstant.StandardBooleanTrueField("Активен")
    is_canceled: DTOConstant.StandardBooleanFalseField("Отменён")
    is_paid: DTOConstant.StandardBooleanFalseField("Оплачен")
    is_refunded: DTOConstant.StandardBooleanFalseField("Возвращён")

    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")
    cancel_refund_reason: DTOConstant.StandardNullableTextField("Причина возврата")
    delivery_date: DTOConstant.StandardNullableDateTimeField("Дата доставки")

    class Config:
        from_attributes = True


class ProductOrderItemRDTO(ProductOrderItemDTO):
    order_id: DTOConstant.StandardUnsignedIntegerField("ID заказа")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса позиции")
    canceled_by_id: DTOConstant.StandardNullableUnsignedIntegerField("ID отменившего пользователя")
    product_id: DTOConstant.StandardUnsignedIntegerField("ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField("ID варианта")
    from_city_id: DTOConstant.StandardNullableUnsignedIntegerField("ID города отправления")
    to_city_id: DTOConstant.StandardNullableUnsignedIntegerField("ID города прибытия")

    qty: DTOConstant.StandardIntegerField("Количество")
    sku: DTOConstant.StandardNullableVarcharField("SKU товара")
    product_price: DTOConstant.StandardPriceField("Цена продукта")
    delta_price: DTOConstant.StandardZeroDecimalField("Изменение цены")
    shipping_price: DTOConstant.StandardZeroDecimalField("Стоимость доставки")
    unit_price: DTOConstant.StandardDecimalField("Итоговая цена за единицу с доставкой")
    total_price: DTOConstant.StandardDecimalField("Итоговая цена за количество с доставкой")

    refunded_total: DTOConstant.StandardZeroDecimalField("Возвращённая сумма")
    is_active: DTOConstant.StandardBooleanTrueField("Активен")
    is_canceled: DTOConstant.StandardBooleanFalseField("Отменён")
    is_paid: DTOConstant.StandardBooleanFalseField("Оплачен")
    is_refunded: DTOConstant.StandardBooleanFalseField("Возвращён")

    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")
    cancel_refund_reason: DTOConstant.StandardNullableTextField("Причина возврата")
    delivery_date: DTOConstant.StandardNullableDateTimeField("Дата доставки")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductOrderItemWithRelationsRDTO(ProductOrderItemRDTO):
    order: Optional["ProductOrderRDTO"] = None
    status: Optional["ProductOrderItemStatusRDTO"] = None
    canceled_by: Optional["UserRDTO"] = None
    product: Optional["ProductRDTO"] = None
    variant: Optional["ProductVariantRDTO"] = None
    from_city: Optional["CityRDTO"] = None
    to_city: Optional["CityRDTO"] = None
    history_records: List["ProductOrderItemHistoryRDTO"] = []

    class Config:
        from_attributes = True
