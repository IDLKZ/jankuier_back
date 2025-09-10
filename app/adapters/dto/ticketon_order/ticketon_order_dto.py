from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Any

from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusRDTO
from app.shared.dto_constants import DTOConstant


class TicketonOrderDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class TicketonOrderCDTO(BaseModel):
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID статуса")
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    show: DTOConstant.StandardVarcharField(description="Шоу")
    seats: DTOConstant.StandardNullableStringArrayField(description="Места")
    lang: DTOConstant.StandardVarcharField(description="Язык")
    pre_sale: DTOConstant.StandardNullableVarcharField(description="Предпродажа")
    sale: DTOConstant.StandardNullableVarcharField(description="Продажа")
    reservation_id: DTOConstant.StandardNullableVarcharField(description="ID бронирования")
    price: DTOConstant.StandardNullablePriceField(description="Цена")
    expire: DTOConstant.StandardNullableIntegerField(description="Время истечения")
    expired_at: DTOConstant.StandardNullableDateTimeField(description="Дата истечения")
    sum: DTOConstant.StandardNullablePriceField(description="Сумма")
    currency: DTOConstant.StandardNullableVarcharField(description="Валюта")
    pre_tickets: List[dict] | None = Field(default=None, description="Предварительные билеты")
    tickets: List[dict] | None = Field(default=None, description="Билеты")
    sale_secury_token: DTOConstant.StandardNullableVarcharField(
        description="Токен безопасности продажи"
    )
    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачен")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Отменен")
    cancel_reason: DTOConstant.StandardNullableVarcharField(description="Причина отмены")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    status: DTOConstant.StandardNullableVarcharField(description="Статус")

    class Config:
        from_attributes = True


class TicketonOrderRDTO(TicketonOrderDTO):
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID статуса")
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    payment_transaction_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID платежной транзакции"
    )
    show: DTOConstant.StandardVarcharField(description="Шоу")
    seats: DTOConstant.StandardNullableStringArrayField(description="Места")
    lang: DTOConstant.StandardVarcharField(description="Язык")
    pre_sale: DTOConstant.StandardNullableVarcharField(description="Предпродажа")
    sale: DTOConstant.StandardNullableVarcharField(description="Продажа")
    reservation_id: DTOConstant.StandardNullableVarcharField(description="ID бронирования")
    price: DTOConstant.StandardNullablePriceField(description="Цена")
    expire: DTOConstant.StandardNullableIntegerField(description="Время истечения")
    expired_at: DTOConstant.StandardNullableDateTimeField(description="Дата истечения")
    sum: DTOConstant.StandardNullablePriceField(description="Сумма")
    currency: DTOConstant.StandardNullableVarcharField(description="Валюта")
    pre_tickets: List[dict] | None = Field(default=None, description="Предварительные билеты")
    tickets: List[dict] | None = Field(default=None, description="Билеты")
    sale_secury_token: DTOConstant.StandardNullableVarcharField(
        description="Токен безопасности продажи"
    )
    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачен")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Отменен")
    cancel_reason: DTOConstant.StandardNullableVarcharField(description="Причина отмены")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    status: DTOConstant.StandardNullableVarcharField(description="Статус")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class TicketonOrderWithRelationsRDTO(TicketonOrderRDTO):
    status: TicketonOrderStatusRDTO | None = None
    user: UserRDTO | None = None
    payment_transaction: PaymentTransactionRDTO | None = None

    class Config:
        from_attributes = True