from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class ProductCategoryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class ProductCategoryCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения категории"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название категории на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название категории на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название категории на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание категории на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание категории на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание категории на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение категории"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности категории"
    )

    class Config:
        from_attributes = True


class ProductCategoryRDTO(ProductCategoryDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID изображения категории"
    )
    title_ru: DTOConstant.StandardVarcharField(
        description="Название категории на русском"
    )
    title_kk: DTOConstant.StandardNullableVarcharField(
        description="Название категории на казахском"
    )
    title_en: DTOConstant.StandardNullableVarcharField(
        description="Название категории на английском"
    )
    description_ru: DTOConstant.StandardNullableTextField(
        description="Описание категории на русском"
    )
    description_kk: DTOConstant.StandardNullableTextField(
        description="Описание категории на казахском"
    )
    description_en: DTOConstant.StandardNullableTextField(
        description="Описание категории на английском"
    )
    value: DTOConstant.StandardUniqueValueField(
        description="Уникальное значение категории"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Флаг активности категории"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class ProductCategoryWithRelationsRDTO(ProductCategoryRDTO):
    image: FileRDTO | None = None

    class Config:
        from_attributes = True
