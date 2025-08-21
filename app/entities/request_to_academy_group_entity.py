from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class RequestToAcademyGroupEntity(Base):
    __tablename__ = AppTableNames.RequestToAcademyGroupTableName

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
    checked_by: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    status: Mapped[
        DbColumnConstants.StandardInteger
    ]  # 0 = not_view, 1 = accepted, -1 = rejected
    info: Mapped[DbColumnConstants.StandardNullableText]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    student: Mapped[AppEntityNames.StudentEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.StudentEntityName,
            back_populates="request_to_academy_groups",
            foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.student_id",
        )
    )

    group: Mapped[AppEntityNames.AcademyGroupEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.AcademyGroupEntityName,
            back_populates="request_to_academy_groups",
            foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.group_id",
        )
    )

    checked_by_user: Mapped[AppEntityNames.UserEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.UserEntityName,
            back_populates="checked_requests_to_academy_groups",
            foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.checked_by",
        )
    )

    academy_group_students: Mapped[
        list[AppEntityNames.AcademyGroupStudentEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.AcademyGroupStudentEntityName,
        back_populates="request",
        foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.request_id",
    )

    request_materials: Mapped[list[AppEntityNames.RequestMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RequestMaterialEntityName,
            back_populates="request",
            foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.request_id",
        )
    )
