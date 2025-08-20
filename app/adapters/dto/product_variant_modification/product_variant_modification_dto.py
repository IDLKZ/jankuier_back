from pydantic import BaseModel
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueRDTO
from app.shared.dto_constants import DTOConstant


class ProductVariantModificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductVariantModificationCDTO(BaseModel):
    variant_id: DTOConstant.StandardUnsignedIntegerField(description="ID варианта товара")
    modification_value_id: DTOConstant.StandardUnsignedIntegerField(description="ID значения модификации")

    class Config:
        from_attributes = True


class ProductVariantModificationRDTO(ProductVariantModificationDTO):
    variant_id: DTOConstant.StandardUnsignedIntegerField(description="ID варианта товара")
    modification_value_id: DTOConstant.StandardUnsignedIntegerField(description="ID значения модификации")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductVariantModificationWithRelationsRDTO(ProductVariantModificationRDTO):
    variant: ProductVariantRDTO | None = None
    modification_value: ModificationValueRDTO | None = None

    class Config:
        from_attributes = True


class ProductVariantModificationBulkCDTO(BaseModel):
    """DTO для массового создания модификаций варианта товара"""
    variant_id: DTOConstant.StandardUnsignedIntegerField(description="ID варианта товара")
    modification_value_ids: list[DTOConstant.StandardUnsignedIntegerField(description="ID значения модификации")] = []

    class Config:
        from_attributes = True


class ProductVariantModificationSummaryDTO(BaseModel):
    """DTO для краткого представления модификаций варианта"""
    variant_id: DTOConstant.StandardUnsignedIntegerField(description="ID варианта товара")
    modifications: list[ModificationValueRDTO] = []

    class Config:
        from_attributes = True