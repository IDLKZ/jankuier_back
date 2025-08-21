from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductVariantEntity(Base):
    __tablename__ = AppTableNames.ProductVariantTableName

    id: Mapped[DbColumnConstants.ID]

    product_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
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

    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    value: Mapped[DbColumnConstants.StandardUniqueValue]
    sku: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    price_delta: Mapped[DbColumnConstants.StandardNullablePrice]
    stock: Mapped[DbColumnConstants.StandardIntegerDefaultZero]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_default: Mapped[DbColumnConstants.StandardBooleanFalse]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    product: Mapped[AppEntityNames.ProductEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.ProductEntityName,
            back_populates="product_variants",
            foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.product_id",
        )
    )

    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="product_variants",
        foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.image_id",
    )

    city: Mapped[AppEntityNames.CityEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        back_populates="product_variants",
        foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.city_id",
    )

    product_variant_modifications: Mapped[
        list[AppEntityNames.ProductVariantModificationEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductVariantModificationEntityName,
        back_populates="variant",
        foreign_keys=f"{AppEntityNames.ProductVariantModificationEntityName}.variant_id",
    )

    cart_items: Mapped[list[AppEntityNames.CartItemEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.CartItemEntityName,
            back_populates="variant",
            foreign_keys=f"{AppEntityNames.CartItemEntityName}.variant_id",
        )
    )

    product_galleries: Mapped[list[AppEntityNames.ProductGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductGalleryEntityName,
            back_populates="variant",
            foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.variant_id",
        )
    )
