from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class RequestMaterialEntity(Base):
    __tablename__ = AppTableNames.RequestMaterialTableName

    id: Mapped[DbColumnConstants.ID]

    title: Mapped[DbColumnConstants.StandardVarchar]

    request_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.RequestToAcademyGroupTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    student_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.StudentTableName, onupdate="CASCADE", ondelete="CASCADE"
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
    request: Mapped[AppEntityNames.RequestToAcademyGroupEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.RequestToAcademyGroupEntityName,
            back_populates="request_materials",
            foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.request_id",
        )
    )

    student: Mapped[AppEntityNames.StudentEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.StudentEntityName,
            back_populates="request_materials",
            foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.student_id",
        )
    )

    file: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="request_materials",
        foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.file_id",
    )
