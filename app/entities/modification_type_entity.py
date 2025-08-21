from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ModificationTypeEntity(Base):
    __tablename__ = AppTableNames.ModificationTypeTableName

    id: Mapped[DbColumnConstants.ID]

    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    value: Mapped[DbColumnConstants.StandardUniqueValue]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    category_modifications: Mapped[
        list[AppEntityNames.CategoryModificationEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.CategoryModificationEntityName,
        back_populates="modification_type",
        foreign_keys=f"{AppEntityNames.CategoryModificationEntityName}.modification_type_id",
    )

    modification_values: Mapped[list[AppEntityNames.ModificationValueEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ModificationValueEntityName,
            back_populates="modification_type",
            foreign_keys=f"{AppEntityNames.ModificationValueEntityName}.modification_type_id",
        )
    )
