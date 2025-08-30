from typing import List
from pydantic import BaseModel

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryWithRelationsRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantWithRelationsRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO
from app.adapters.dto.modification_type.modification_type_dto import ModificationTypeRDTO
from app.adapters.dto.product_variant_modification.product_variant_modification_dto import \
    ProductVariantModificationWithRelationsRDTO


class FullProductRDTO(BaseModel):
    """DTO для полной информации о товаре со всеми связанными данными"""
    
    product: ProductWithRelationsRDTO
    galleries: List[ProductGalleryWithRelationsRDTO]
    variants: List[ProductVariantWithRelationsRDTO] 
    modification_values: List[ModificationValueWithRelationsRDTO]
    modification_types: List[ModificationTypeRDTO]
    product_variant_modifications: List[ProductVariantModificationWithRelationsRDTO]

    class Config:
        from_attributes = True