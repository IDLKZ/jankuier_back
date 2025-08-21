from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbRelationshipConstants, DbColumnConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductVariantModificationEntity(Base):
    __tablename__ = AppTableNames.ProductVariantModificationTableName

    id: Mapped[DbColumnConstants.ID]

    variant_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductVariantTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    modification_value_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ModificationValueTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    variant: Mapped[AppEntityNames.ProductVariantEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.ProductVariantEntityName,
            back_populates="product_variant_modifications",
            foreign_keys=f"{AppEntityNames.ProductVariantModificationEntityName}.variant_id",
        )
    )

    modification_value: Mapped[AppEntityNames.ModificationValueEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.ModificationValueEntityName,
            back_populates="product_variant_modifications",
            foreign_keys=f"{AppEntityNames.ProductVariantModificationEntityName}.modification_value_id",
        )
    )
