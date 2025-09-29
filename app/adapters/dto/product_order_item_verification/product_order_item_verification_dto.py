from typing import Optional
from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant

class ProductOrderItemVerificationCodeDTO(BaseModel):
    id: DTOConstant.StandardID("ID кода верификации")

    class Config:
        from_attributes = True



class ProductOrderItemVerificationCodeCDTO(BaseModel):
    order_item_id: DTOConstant.StandardUnsignedIntegerField("ID позиции заказа")
    responsible_user_id: DTOConstant.StandardNullableUnsignedIntegerField("ID ответственного пользователя")
    code: DTOConstant.StandardVarcharField("Код верификации")
    is_active: DTOConstant.StandardBooleanTrueField("Флаг активности")

    class Config:
        from_attributes = True


class ProductOrderItemVerificationCodeRDTO(ProductOrderItemVerificationCodeDTO):
    order_item_id: DTOConstant.StandardUnsignedIntegerField("ID позиции заказа")
    responsible_user_id: DTOConstant.StandardNullableUnsignedIntegerField("ID ответственного пользователя")
    code: DTOConstant.StandardVarcharField("Код верификации")
    is_active: DTOConstant.StandardBooleanTrueField("Флаг активности")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class ProductOrderItemVerificationCodeWithRelationsRDTO(ProductOrderItemVerificationCodeRDTO):
    order_item: Optional["ProductOrderItemRDTO"] = None
    responsible_user: Optional["UserRDTO"] = None

    class Config:
        from_attributes = True
