from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductGalleryEntity(Base):
    __tablename__ = AppTableNames.ProductGalleryTableName

    id: Mapped[DbColumnConstants.ID]

    product_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    variant_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductVariantTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    product: Mapped[AppEntityNames.ProductEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.ProductEntityName,
            back_populates="product_galleries",
            foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.product_id",
        )
    )

    variant: Mapped[AppEntityNames.ProductVariantEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.ProductVariantEntityName,
            back_populates="product_galleries",
            foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.variant_id",
        )
    )

    file: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="product_galleries",
        foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.file_id",
    )
