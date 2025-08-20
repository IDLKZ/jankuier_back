from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class StudentEntity(Base):
    __tablename__ = AppTableNames.StudentTableName

    id: Mapped[DbColumnConstants.ID]

    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    created_by: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    first_name: Mapped[DbColumnConstants.StandardVarchar]
    last_name: Mapped[DbColumnConstants.StandardVarchar]
    patronymic: Mapped[DbColumnConstants.StandardNullableVarchar]

    birthdate: Mapped[DbColumnConstants.StandardDate]
    reschedule_end_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    gender: Mapped[DbColumnConstants.StandardTinyInteger]  # 0 both, 1 male, 2 female

    phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    additional_phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardNullableVarchar]

    info: Mapped[DbColumnConstants.StandardNullableText]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="students",
        foreign_keys=f"{AppEntityNames.StudentEntityName}.image_id",
    )

    created_by_user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="created_students",
        foreign_keys=f"{AppEntityNames.StudentEntityName}.created_by",
    )

    academy_group_students: Mapped[list[AppEntityNames.AcademyGroupStudentEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGroupStudentEntityName,
            back_populates="student",
            foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.student_id",
        )
    )

    request_to_academy_groups: Mapped[list[AppEntityNames.RequestToAcademyGroupEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RequestToAcademyGroupEntityName,
            back_populates="student",
            foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.student_id",
        )
    )

    request_materials: Mapped[list[AppEntityNames.RequestMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RequestMaterialEntityName,
            back_populates="student",
            foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.student_id",
        )
    )

