from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ModificationValueEntity(Base):
    __tablename__ = AppTableNames.ModificationValueTableName

    id: Mapped[DbColumnConstants.ID]

    modification_type_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ModificationTypeTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    product_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    description_ru: Mapped[DbColumnConstants.StandardNullableText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    modification_type: Mapped[AppEntityNames.ModificationTypeEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ModificationTypeEntityName,
        back_populates="modification_values",
        foreign_keys=f"{AppEntityNames.ModificationValueEntityName}.modification_type_id",
    )

    product: Mapped[AppEntityNames.ProductEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductEntityName,
        back_populates="modification_values",
        foreign_keys=f"{AppEntityNames.ModificationValueEntityName}.product_id",
    )

    product_variant_modifications: Mapped[list[AppEntityNames.ProductVariantModificationEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductVariantModificationEntityName,
            back_populates="modification_value",
            foreign_keys=f"{AppEntityNames.ProductVariantModificationEntityName}.modification_value_id",
        )
    )