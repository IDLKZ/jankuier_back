from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class AcademyGroupStudentEntity(Base):
    __tablename__ = AppTableNames.AcademyGroupStudentTableName

    id: Mapped[DbColumnConstants.ID]

    student_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.StudentTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    group_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.AcademyGroupTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    request_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.RequestToAcademyGroupTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    info: Mapped[DbColumnConstants.StandardNullableText]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    student: Mapped[AppEntityNames.StudentEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.StudentEntityName,
            back_populates="academy_group_students",
            foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.student_id",
        )
    )

    group: Mapped[AppEntityNames.AcademyGroupEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.AcademyGroupEntityName,
            back_populates="academy_group_students",
            foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.group_id",
        )
    )

    request: Mapped[AppEntityNames.RequestToAcademyGroupEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.RequestToAcademyGroupEntityName,
            back_populates="academy_group_students",
            foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.request_id",
        )
    )
