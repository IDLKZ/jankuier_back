from pydantic import BaseModel
from datetime import datetime

from app.adapters.dto.user.user_dto import UserRDTO
from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusRDTO
from app.shared.dto_constants import DTOConstant


class PaymentTransactionDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class PaymentTransactionCDTO(BaseModel):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID статуса")
    transaction_type: DTOConstant.StandardVarcharField(description="Тип транзакции")
    order: DTOConstant.StandardVarcharField(description="Номер заказа")
    mpi_order: DTOConstant.StandardNullableVarcharField(description="MPI заказ")
    amount: DTOConstant.StandardPriceField(description="Сумма")
    currency: DTOConstant.StandardVarcharField(description="Валюта")
    merchant: DTOConstant.StandardVarcharField(description="Мерчант")
    language: DTOConstant.StandardNullableVarcharField(description="Язык")
    client_id: DTOConstant.StandardNullableIntegerField(description="ID клиента")
    desc: DTOConstant.StandardVarcharField(description="Описание")
    desc_order: DTOConstant.StandardNullableTextField(description="Описание заказа")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    backref: DTOConstant.StandardNullableTextField(description="Обратная ссылка")
    wtype: DTOConstant.StandardNullableVarcharField(description="Тип виджета")
    name: DTOConstant.StandardNullableVarcharField(description="Имя")
    pre_p_sign: DTOConstant.StandardNullableTextField(description="Предварительная подпись")
    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачен")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Отменен")
    expired_at: DTOConstant.StandardNullableDateTimeField(description="Время истечения")
    res_code: DTOConstant.StandardNullableVarcharField(description="Код результата")
    res_desc: DTOConstant.StandardNullableTextField(description="Описание результата")
    paid_p_sign: DTOConstant.StandardNullableTextField(description="Подпись оплаты")
    rev_amount: DTOConstant.StandardNullablePriceField(description="Сумма возврата")
    rev_desc: DTOConstant.StandardNullableTextField(description="Описание возврата")
    cancel_p_sign: DTOConstant.StandardNullableTextField(description="Подпись отмены")
    order_full_info: DTOConstant.StandardNullableJSONField(description="Полная информация о заказе")

    class Config:
        from_attributes = True


class PaymentTransactionRDTO(PaymentTransactionDTO):
    user_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID пользователя")
    status_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID статуса")
    transaction_type: DTOConstant.StandardVarcharField(description="Тип транзакции")
    order: DTOConstant.StandardVarcharField(description="Номер заказа")
    mpi_order: DTOConstant.StandardNullableVarcharField(description="MPI заказ")
    amount: DTOConstant.StandardPriceField(description="Сумма")
    currency: DTOConstant.StandardVarcharField(description="Валюта")
    merchant: DTOConstant.StandardVarcharField(description="Мерчант")
    language: DTOConstant.StandardNullableVarcharField(description="Язык")
    client_id: DTOConstant.StandardNullableIntegerField(description="ID клиента")
    desc: DTOConstant.StandardVarcharField(description="Описание")
    desc_order: DTOConstant.StandardNullableTextField(description="Описание заказа")
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    backref: DTOConstant.StandardNullableTextField(description="Обратная ссылка")
    wtype: DTOConstant.StandardNullableVarcharField(description="Тип виджета")
    name: DTOConstant.StandardNullableVarcharField(description="Имя")
    pre_p_sign: DTOConstant.StandardNullableTextField(description="Предварительная подпись")
    is_active: DTOConstant.StandardBooleanFalseField(description="Активен")
    is_paid: DTOConstant.StandardBooleanFalseField(description="Оплачен")
    is_canceled: DTOConstant.StandardBooleanFalseField(description="Отменен")
    expired_at: DTOConstant.StandardNullableDateTimeField(description="Время истечения")
    res_code: DTOConstant.StandardNullableVarcharField(description="Код результата")
    res_desc: DTOConstant.StandardNullableTextField(description="Описание результата")
    paid_p_sign: DTOConstant.StandardNullableTextField(description="Подпись оплаты")
    rev_amount: DTOConstant.StandardNullablePriceField(description="Сумма возврата")
    rev_desc: DTOConstant.StandardNullableTextField(description="Описание возврата")
    cancel_p_sign: DTOConstant.StandardNullableTextField(description="Подпись отмены")
    order_full_info: DTOConstant.StandardNullableJSONField(description="Полная информация о заказе")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class PaymentTransactionWithRelationsRDTO(PaymentTransactionRDTO):
    user: UserRDTO | None = None
    status: PaymentTransactionStatusRDTO | None = None

    class Config:
        from_attributes = True