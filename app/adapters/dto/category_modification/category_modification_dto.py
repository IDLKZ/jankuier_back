from pydantic import BaseModel
from app.adapters.dto.product_category.product_category_dto import ProductCategoryRDTO
from app.adapters.dto.modification_type.modification_type_dto import ModificationTypeRDTO
from app.shared.dto_constants import DTOConstant


class CategoryModificationDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class CategoryModificationCDTO(BaseModel):
    category_id: DTOConstant.StandardUnsignedIntegerField(description="ID категории товара")
    modification_type_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID типа модификации")

    class Config:
        from_attributes = True


class CategoryModificationRDTO(CategoryModificationDTO):
    category_id: DTOConstant.StandardUnsignedIntegerField(description="ID категории товара")
    modification_type_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID типа модификации")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class CategoryModificationWithRelationsRDTO(CategoryModificationRDTO):
    category: ProductCategoryRDTO | None = None
    modification_type: ModificationTypeRDTO | None = None

    class Config:
        from_attributes = True


class CategoryModificationBulkCDTO(BaseModel):
    """DTO для массового создания модификаций категории"""
    category_id: DTOConstant.StandardUnsignedIntegerField(description="ID категории товара")
    modification_type_ids: list[DTOConstant.StandardUnsignedIntegerField(description="ID типа модификации")] = []

    class Config:
        from_attributes = True