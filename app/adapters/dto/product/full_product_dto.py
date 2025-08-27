from typing import List
from pydantic import BaseModel

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryWithRelationsRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantWithRelationsRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO


class FullProductRDTO(BaseModel):
    """DTO для полной информации о товаре со всеми связанными данными"""
    
    product: ProductWithRelationsRDTO
    galleries: List[ProductGalleryWithRelationsRDTO]
    variants: List[ProductVariantWithRelationsRDTO] 
    modification_values: List[ModificationValueWithRelationsRDTO]
    
    class Config:
        from_attributes = True