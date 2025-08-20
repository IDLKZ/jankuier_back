from pydantic import BaseModel
from app.adapters.dto.modification_type.modification_type_dto import ModificationTypeRDTO
from app.adapters.dto.product.product_dto import ProductRDTO
from app.shared.dto_constants import DTOConstant


class ModificationValueDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ModificationValueCDTO(BaseModel):
    modification_type_id: DTOConstant.StandardUnsignedIntegerField(description="ID типа модификации")
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    title_ru: DTOConstant.StandardVarcharField(description="Название значения модификации на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание значения модификации на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание значения модификации на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание значения модификации на английском")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности значения модификации")

    class Config:
        from_attributes = True


class ModificationValueRDTO(ModificationValueDTO):
    modification_type_id: DTOConstant.StandardUnsignedIntegerField(description="ID типа модификации")
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    title_ru: DTOConstant.StandardVarcharField(description="Название значения модификации на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание значения модификации на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание значения модификации на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание значения модификации на английском")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности значения модификации")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ModificationValueWithRelationsRDTO(ModificationValueRDTO):
    modification_type: ModificationTypeRDTO | None = None
    product: ProductRDTO | None = None

    class Config:
        from_attributes = True


class ModificationValueUpdateDTO(BaseModel):
    """DTO для обновления значения модификации - все поля опциональные кроме ID связей"""
    title_ru: DTOConstant.StandardVarcharField(description="Название значения модификации на русском") | None = None
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на казахском") | None = None
    title_en: DTOConstant.StandardNullableVarcharField(description="Название значения модификации на английском") | None = None
    description_ru: DTOConstant.StandardNullableTextField(description="Описание значения модификации на русском") | None = None
    description_kk: DTOConstant.StandardNullableTextField(description="Описание значения модификации на казахском") | None = None
    description_en: DTOConstant.StandardNullableTextField(description="Описание значения модификации на английском") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности значения модификации") | None = None

    class Config:
        from_attributes = True