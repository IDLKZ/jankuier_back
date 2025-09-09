from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class PaymentTransactionStatusDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class PaymentTransactionStatusCDTO(BaseModel):
    previous_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID предыдущего статуса"
    )
    next_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID следующего статуса"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название статуса на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на английском"
    )
    is_first: DTOConstant.StandardBooleanFalseField(
        description="Является ли первым статусом"
    )
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(
        description="Является ли последним статусом"
    )

    class Config:
        from_attributes = True


class PaymentTransactionStatusRDTO(PaymentTransactionStatusDTO):
    previous_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID предыдущего статуса"
    )
    next_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID следующего статуса"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название статуса на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название статуса на английском"
    )
    is_first: DTOConstant.StandardBooleanFalseField(
        description="Является ли первым статусом"
    )
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(
        description="Является ли последним статусом"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class PaymentTransactionStatusWithRelationsRDTO(PaymentTransactionStatusRDTO):
    previous_status: "PaymentTransactionStatusRDTO | None" = None
    next_status: "PaymentTransactionStatusRDTO | None" = None

    class Config:
        from_attributes = True