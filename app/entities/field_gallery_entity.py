from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FieldGalleryEntity(Base):
    __tablename__ = AppTableNames.FieldGalleryTableName

    id: Mapped[DbColumnConstants.ID]

    field_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FieldTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    party_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FieldPartyTableName,
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
    field: Mapped[AppEntityNames.FieldEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldEntityName,
        back_populates="field_galleries",
        foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.field_id",
    )

    party: Mapped[AppEntityNames.FieldPartyEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.FieldPartyEntityName,
            back_populates="field_galleries",
            foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.party_id",
        )
    )

    file: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="field_galleries",
        foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.file_id",
    )
