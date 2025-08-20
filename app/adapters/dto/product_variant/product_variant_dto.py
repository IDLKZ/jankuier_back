from pydantic import BaseModel
from app.adapters.dto.product.product_dto import ProductRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.city.city_dto import CityRDTO
from app.shared.dto_constants import DTOConstant


class ProductVariantDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductVariantCDTO(BaseModel):
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения варианта")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название варианта на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название варианта на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название варианта на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение варианта")
    sku: DTOConstant.StandardNullableVarcharField(description="SKU варианта товара")
    price_delta: DTOConstant.StandardNullablePriceField(description="Изменение цены относительно базовой")
    stock: DTOConstant.StandardIntegerField(description="Количество на складе")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности варианта")
    is_default: DTOConstant.StandardBooleanFalseField(description="Вариант по умолчанию")

    class Config:
        from_attributes = True


class ProductVariantRDTO(ProductVariantDTO):
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения варианта")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    title_ru: DTOConstant.StandardVarcharField(description="Название варианта на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название варианта на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название варианта на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение варианта")
    sku: DTOConstant.StandardNullableVarcharField(description="SKU варианта товара")
    price_delta: DTOConstant.StandardNullablePriceField(description="Изменение цены относительно базовой")
    stock: DTOConstant.StandardIntegerField(description="Количество на складе")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности варианта")
    is_default: DTOConstant.StandardBooleanFalseField(description="Вариант по умолчанию")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductVariantWithRelationsRDTO(ProductVariantRDTO):
    product: ProductRDTO | None = None
    image: FileRDTO | None = None
    city: CityRDTO | None = None

    class Config:
        from_attributes = True


class ProductVariantUpdateDTO(BaseModel):
    """DTO для обновления варианта товара - все поля опциональные"""
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID изображения варианта") | None = None
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города") | None = None
    title_ru: DTOConstant.StandardVarcharField(description="Название варианта на русском") | None = None
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название варианта на казахском") | None = None
    title_en: DTOConstant.StandardNullableVarcharField(description="Название варианта на английском") | None = None
    sku: DTOConstant.StandardNullableVarcharField(description="SKU варианта товара") | None = None
    price_delta: DTOConstant.StandardNullablePriceField(description="Изменение цены относительно базовой") | None = None
    stock: DTOConstant.StandardIntegerField(description="Количество на складе") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности варианта") | None = None
    is_default: DTOConstant.StandardBooleanFalseField(description="Вариант по умолчанию") | None = None

    class Config:
        from_attributes = True