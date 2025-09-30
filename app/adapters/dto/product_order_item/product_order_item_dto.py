from typing import Optional, List
from pydantic import BaseModel, Field
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


class ChangeDeliveryProductOrderItemCDTO(BaseModel):
    """
    DTO для изменения статуса доставки ProductOrderItem.

    Используется для двух действий:
    1. "Принять в обработку" - заполняется только responsible_user_id
    2. "Принять решение" - заполняются все поля с is_passed и новым статусом

    Fields:
        is_passed: True - успешное прохождение этапа, False - отмена/отклонение, None - только взятие в работу
        new_status_id: Новый статус для ProductOrderItem (применяется только при is_passed=True)
        message_ru: Сообщение на русском для записи в историю
        message_kk: Сообщение на казахском для записи в историю
        message_en: Сообщение на английском для истории
        cancel_reason: Причина отмены (обязательно при is_passed=False)
        verification_code: Код верификации (обязателен для статуса "Успешно получен")
    """
    is_passed: Optional[bool] = Field(
        default=None,
        description="Результат прохождения этапа: True - успех, False - отмена, None - только взятие в работу"
    )
    new_status_id: Optional[int] = Field(
        default=None,
        description="Новый статус для ProductOrderItem"
    )
    message_ru: Optional[str] = Field(
        default=None,
        description="Сообщение на русском для истории"
    )
    message_kk: Optional[str] = Field(
        default=None,
        description="Сообщение на казахском для истории"
    )
    message_en: Optional[str] = Field(
        default=None,
        description="Сообщение на английском для истории"
    )
    cancel_reason: Optional[str] = Field(
        default=None,
        description="Причина отмены (обязательно при is_passed=False)"
    )
    verification_code: Optional[str] = Field(
        default=None,
        description="Код верификации (обязателен для статуса 'Успешно получен')"
    )

    class Config:
        from_attributes = True
