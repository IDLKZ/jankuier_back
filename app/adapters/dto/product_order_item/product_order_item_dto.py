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
    from_city_id: DTOConstant.StandardUnsignedIntegerField("ID города отправления")
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
    from_city_id: DTOConstant.StandardUnsignedIntegerField("ID города отправления")
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
    order: "ProductOrderRDTO" | None = None
    status: "ProductOrderItemStatusRDTO" | None = None
    canceled_by: "UserRDTO" | None = None
    product: "ProductRDTO" | None = None
    variant: "ProductVariantRDTO" | None = None
    from_city: "CityRDTO" | None = None
    to_city: "CityRDTO" | None = None
    history_records: list["ProductOrderItemHistoryRDTO"] = []

    class Config:
        from_attributes = True
