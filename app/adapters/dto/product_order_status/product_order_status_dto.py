from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class ProductOrderStatusDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductOrderStatusCDTO(BaseModel):
    previous_id: DTOConstant.StandardNullableIntegerField(description="ID предыдущего статуса")
    next_id: DTOConstant.StandardNullableIntegerField(description="ID следующего статуса")
    title_ru: DTOConstant.StandardVarcharField(description="Название статуса на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название статуса на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название статуса на английском")
    is_first: DTOConstant.StandardBooleanFalseField(description="Первый статус в цепочке")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(description="Последний статус в цепочке")
    previous_allowed_values: DTOConstant.StandardNullableStringArrayField(description="Разрешенные предыдущие значения")
    next_allowed_values: DTOConstant.StandardNullableStringArrayField(description="Разрешенные следующие значения")

    class Config:
        from_attributes = True


class ProductOrderStatusRDTO(ProductOrderStatusDTO):
    previous_id: DTOConstant.StandardNullableIntegerField(description="ID предыдущего статуса")
    next_id: DTOConstant.StandardNullableIntegerField(description="ID следующего статуса")
    title_ru: DTOConstant.StandardVarcharField(description="Название статуса на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название статуса на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название статуса на английском")
    is_first: DTOConstant.StandardBooleanFalseField(description="Первый статус в цепочке")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности")
    is_last: DTOConstant.StandardBooleanFalseField(description="Последний статус в цепочке")
    previous_allowed_values: DTOConstant.StandardNullableStringArrayField(description="Разрешенные предыдущие значения")
    next_allowed_values: DTOConstant.StandardNullableStringArrayField(description="Разрешенные следующие значения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductOrderStatusWithRelationsRDTO(ProductOrderStatusRDTO):
    previous_status: "ProductOrderStatusRDTO | None" = None
    next_status: "ProductOrderStatusRDTO | None" = None

    class Config:
        from_attributes = True