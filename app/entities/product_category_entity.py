from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductCategoryEntity(Base):
    __tablename__ = AppTableNames.ProductCategoryTableName
    id: Mapped[DbColumnConstants.ID]
    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
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
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="product_categories",
        foreign_keys=f"{AppEntityNames.ProductCategoryEntityName}.image_id",
    )

    products: Mapped[list[AppEntityNames.ProductEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductEntityName,
            back_populates="category",
            foreign_keys=f"{AppEntityNames.ProductEntityName}.category_id",
        )
    )

    category_modifications: Mapped[
        list[AppEntityNames.CategoryModificationEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.CategoryModificationEntityName,
        back_populates="category",
        foreign_keys=f"{AppEntityNames.CategoryModificationEntityName}.category_id",
    )
