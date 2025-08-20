from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductEntity(Base):
    __tablename__ = AppTableNames.ProductTableName

    id: Mapped[DbColumnConstants.ID]
    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    city_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.CityTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    category_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductCategoryTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    description_ru: Mapped[DbColumnConstants.StandardNullableText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]

    value: Mapped[DbColumnConstants.StandardUniqueValue]
    sku: Mapped[DbColumnConstants.StandardUniqueValue]

    base_price: Mapped[DbColumnConstants.StandardPrice]
    old_price: Mapped[DbColumnConstants.StandardNullablePrice]

    gender: Mapped[DbColumnConstants.StandardTinyInteger]  # 0 - unisex, 1 - male, 2 - female
    is_for_children: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_recommended: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="products",
        foreign_keys=f"{AppEntityNames.ProductEntityName}.image_id",
    )

    city: Mapped[AppEntityNames.CityEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        back_populates="products",
        foreign_keys=f"{AppEntityNames.ProductEntityName}.city_id",
    )

    category: Mapped[AppEntityNames.ProductCategoryEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductCategoryEntityName,
        back_populates="products",
        foreign_keys=f"{AppEntityNames.ProductEntityName}.category_id",
    )

    product_variants: Mapped[list[AppEntityNames.ProductVariantEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductVariantEntityName,
            back_populates="product",
            foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.product_id",
        )
    )

    product_galleries: Mapped[list[AppEntityNames.ProductGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductGalleryEntityName,
            back_populates="product",
            foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.product_id",
        )
    )

    cart_items: Mapped[list[AppEntityNames.CartItemEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.CartItemEntityName,
            back_populates="product",
            foreign_keys=f"{AppEntityNames.CartItemEntityName}.product_id",
        )
    )

    modification_values: Mapped[list[AppEntityNames.ModificationValueEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ModificationValueEntityName,
            back_populates="product",
            foreign_keys=f"{AppEntityNames.ModificationValueEntityName}.product_id",
        )
    )
