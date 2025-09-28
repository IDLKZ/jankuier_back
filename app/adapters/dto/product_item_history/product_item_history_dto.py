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

    message_ru: DTOConstant.StandardNullableVarcharField("Сообщение (RU)")
    message_kk: DTOConstant.StandardNullableVarcharField("Сообщение (KK)")
    message_en: DTOConstant.StandardNullableVarcharField("Сообщение (EN)")

    is_passed: DTOConstant.StandardNullableBooleanField("Флаг прохождения")
    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")

    taken_at: DTOConstant.StandardNullableDateTimeField("Дата взятия")
    passed_at: DTOConstant.StandardNullableDateTimeField("Дата прохождения")

    class Config:
        from_attributes = True



class ProductOrderItemHistoryRDTO(ProductOrderItemHistoryDTO):
    order_item_id: DTOConstant.StandardUnsignedIntegerField("ID позиции заказа")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField("ID статуса")
    responsible_user_id: DTOConstant.StandardNullableUnsignedIntegerField("ID ответственного пользователя")

    message_ru: DTOConstant.StandardNullableVarcharField("Сообщение (RU)")
    message_kk: DTOConstant.StandardNullableVarcharField("Сообщение (KK)")
    message_en: DTOConstant.StandardNullableVarcharField("Сообщение (EN)")

    is_passed: DTOConstant.StandardNullableBooleanField("Флаг прохождения")
    cancel_reason: DTOConstant.StandardNullableTextField("Причина отмены")

    taken_at: DTOConstant.StandardNullableDateTimeField("Дата взятия")
    passed_at: DTOConstant.StandardNullableDateTimeField("Дата прохождения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductOrderItemHistoryWithRelationsRDTO(ProductOrderItemHistoryRDTO):
    order_item: "ProductOrderItemRDTO" | None = None
    status: "ProductOrderItemStatusRDTO" | None = None
    responsible_user: "UserRDTO" | None = None

    class Config:
        from_attributes = True
