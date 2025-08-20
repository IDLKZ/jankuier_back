from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class CategoryModificationEntity(Base):
    __tablename__ = AppTableNames.CategoryModificationTableName

    id: Mapped[DbColumnConstants.ID]

    category_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductCategoryTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    modification_type_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ModificationTypeTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    category: Mapped[AppEntityNames.ProductCategoryEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductCategoryEntityName,
        back_populates="category_modifications",
        foreign_keys=f"{AppEntityNames.CategoryModificationEntityName}.category_id",
    )

    modification_type: Mapped[AppEntityNames.ModificationTypeEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ModificationTypeEntityName,
        back_populates="category_modifications",
        foreign_keys=f"{AppEntityNames.CategoryModificationEntityName}.modification_type_id",
    )


