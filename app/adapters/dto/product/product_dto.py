from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.city.city_dto import CityRDTO
from app.adapters.dto.product_category.product_category_dto import ProductCategoryRDTO
from app.shared.dto_constants import DTOConstant


class ProductDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения товара")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    category_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID категории товара")
    title_ru: DTOConstant.StandardVarcharField(description="Название товара на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название товара на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название товара на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание товара на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание товара на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание товара на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение товара")
    sku: DTOConstant.StandardUniqueValueField(description="SKU товара")
    base_price: DTOConstant.StandardPriceField(description="Базовая цена товара")
    old_price: DTOConstant.StandardNullablePriceField(description="Старая цена товара")
    gender: DTOConstant.StandardIntegerField(description="Пол: 0-унисекс, 1-мужской, 2-женский")
    is_for_children: DTOConstant.StandardBooleanFalseField(description="Товар для детей")
    is_recommended: DTOConstant.StandardBooleanFalseField(description="Рекомендованный товар")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности товара")

    class Config:
        from_attributes = True


class ProductRDTO(ProductDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения товара")
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города")
    category_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID категории товара")
    title_ru: DTOConstant.StandardVarcharField(description="Название товара на русском")
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название товара на казахском")
    title_en: DTOConstant.StandardNullableVarcharField(description="Название товара на английском")
    description_ru: DTOConstant.StandardNullableTextField(description="Описание товара на русском")
    description_kk: DTOConstant.StandardNullableTextField(description="Описание товара на казахском")
    description_en: DTOConstant.StandardNullableTextField(description="Описание товара на английском")
    value: DTOConstant.StandardUniqueValueField(description="Уникальное значение товара")
    sku: DTOConstant.StandardUniqueValueField(description="SKU товара")
    base_price: DTOConstant.StandardPriceField(description="Базовая цена товара")
    old_price: DTOConstant.StandardNullablePriceField(description="Старая цена товара")
    gender: DTOConstant.StandardIntegerField(description="Пол: 0-унисекс, 1-мужской, 2-женский")
    is_for_children: DTOConstant.StandardBooleanFalseField(description="Товар для детей")
    is_recommended: DTOConstant.StandardBooleanFalseField(description="Рекомендованный товар")
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности товара")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductWithRelationsRDTO(ProductRDTO):
    image: FileRDTO | None = None
    city: CityRDTO | None = None
    category: ProductCategoryRDTO | None = None

    class Config:
        from_attributes = True


class ProductUpdateDTO(BaseModel):
    """DTO для обновления товара - все поля опциональные"""
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID главного изображения товара") | None = None
    city_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID города") | None = None
    category_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID категории товара") | None = None
    title_ru: DTOConstant.StandardVarcharField(description="Название товара на русском") | None = None
    title_kk: DTOConstant.StandardNullableVarcharField(description="Название товара на казахском") | None = None
    title_en: DTOConstant.StandardNullableVarcharField(description="Название товара на английском") | None = None
    description_ru: DTOConstant.StandardNullableTextField(description="Описание товара на русском") | None = None
    description_kk: DTOConstant.StandardNullableTextField(description="Описание товара на казахском") | None = None
    description_en: DTOConstant.StandardNullableTextField(description="Описание товара на английском") | None = None
    base_price: DTOConstant.StandardPriceField(description="Базовая цена товара") | None = None
    old_price: DTOConstant.StandardNullablePriceField(description="Старая цена товара") | None = None
    gender: DTOConstant.StandardIntegerField(description="Пол: 0-унисекс, 1-мужской, 2-женский") | None = None
    is_for_children: DTOConstant.StandardBooleanFalseField(description="Товар для детей") | None = None
    is_recommended: DTOConstant.StandardBooleanFalseField(description="Рекомендованный товар") | None = None
    is_active: DTOConstant.StandardBooleanTrueField(description="Флаг активности товара") | None = None

    class Config:
        from_attributes = True