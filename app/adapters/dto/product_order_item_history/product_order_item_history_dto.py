from typing import Optional
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant

class ProductOrderItemHistoryDTO(BaseModel):
    id: DTOConstant.StandardID("ID записи истории")

    class Config:
        from_attributes = True


class ProductOrderItemHistoryCDTO(BaseModel):
    order_item_id: DTOConstant.StandardUnsignedIntegerField("ID позиции заказа")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса")
    responsible_user_id: DTOConstant.StandardNullableUnsignedIntegerField("ID ответственного пользователя")

    message_ru: DTOConstant.StandardNullableVarcharField("Сообщение на русском")
    message_kk: DTOConstant.StandardNullableVarcharField("Сообщение на казахском")
    message_en: DTOConstant.StandardNullableVarcharField("Сообщение на английском")

    is_passed: DTOConstant.StandardNullableBooleanField("Статус прохождения")
    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")

    taken_at: DTOConstant.StandardNullableDateTimeField("Время взятия в работу")
    passed_at: DTOConstant.StandardNullableDateTimeField("Время прохождения")

    class Config:
        from_attributes = True


class ProductOrderItemHistoryRDTO(ProductOrderItemHistoryDTO):
    order_item_id: DTOConstant.StandardUnsignedIntegerField("ID позиции заказа")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса")
    responsible_user_id: DTOConstant.StandardNullableUnsignedIntegerField("ID ответственного пользователя")

    message_ru: DTOConstant.StandardNullableVarcharField("Сообщение на русском")
    message_kk: DTOConstant.StandardNullableVarcharField("Сообщение на казахском")
    message_en: DTOConstant.StandardNullableVarcharField("Сообщение на английском")

    is_passed: DTOConstant.StandardNullableBooleanField("Статус прохождения")
    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")

    taken_at: DTOConstant.StandardNullableDateTimeField("Время взятия в работу")
    passed_at: DTOConstant.StandardNullableDateTimeField("Время прохождения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductOrderItemHistoryWithRelationsRDTO(ProductOrderItemHistoryRDTO):
    order_item: Optional["ProductOrderItemRDTO"] = None
    status: Optional["ProductOrderItemStatusRDTO"] = None
    responsible_user: Optional["UserRDTO"] = None

    class Config:
        from_attributes = True