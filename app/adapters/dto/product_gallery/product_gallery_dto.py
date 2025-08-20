from pydantic import BaseModel
from app.adapters.dto.product.product_dto import ProductRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class ProductGalleryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductGalleryCDTO(BaseModel):
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID варианта товара (опционально)")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения")

    class Config:
        from_attributes = True


class ProductGalleryRDTO(ProductGalleryDTO):
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID варианта товара (опционально)")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class ProductGalleryWithRelationsRDTO(ProductGalleryRDTO):
    product: ProductRDTO | None = None
    variant: ProductVariantRDTO | None = None
    file: FileRDTO | None = None

    class Config:
        from_attributes = True


class ProductGalleryBulkCDTO(BaseModel):
    """DTO для массового создания изображений галереи"""
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID варианта товара (опционально)") | None = None
    file_ids: list[DTOConstant.StandardUnsignedIntegerField(description="ID файла изображения")] = []

    class Config:
        from_attributes = True


class ProductGalleryUpdateDTO(BaseModel):
    """DTO для обновления изображения в галерее"""
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID варианта товара") | None = None
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения") | None = None

    class Config:
        from_attributes = True