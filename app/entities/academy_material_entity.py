from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class AcademyMaterialEntity(Base):
    __tablename__ = AppTableNames.AcademyMaterialTableName

    id: Mapped[DbColumnConstants.ID]
    title: Mapped[DbColumnConstants.StandardVarchar]

    academy_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.AcademyTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    group_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.AcademyGroupTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    file_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    academy: Mapped[AppEntityNames.AcademyEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.AcademyEntityName,
        back_populates="academy_materials",
        foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.academy_id",
    )

    group: Mapped[AppEntityNames.AcademyGroupEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.AcademyGroupEntityName,
        back_populates="academy_materials",
        foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.group_id",
    )

    file: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="academy_materials",
        foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.file_id",
    )


