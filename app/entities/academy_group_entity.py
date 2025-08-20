from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class AcademyGroupEntity(Base):
    __tablename__ = AppTableNames.AcademyGroupTableName

    id: Mapped[DbColumnConstants.ID]

    academy_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.AcademyTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    name: Mapped[DbColumnConstants.StandardVarchar]

    description_ru: Mapped[DbColumnConstants.StandardNullableText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]

    value: Mapped[DbColumnConstants.StandardUniqueValue]

    min_age: Mapped[DbColumnConstants.StandardInteger]
    max_age: Mapped[DbColumnConstants.StandardInteger]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_recruiting: Mapped[DbColumnConstants.StandardBooleanFalse]

    gender: Mapped[DbColumnConstants.StandardTinyInteger]  # 0 both, 1 male, 2 female

    booked_space: Mapped[DbColumnConstants.StandardIntegerDefaultZero]
    free_space: Mapped[DbColumnConstants.StandardIntegerDefaultZero]

    price: Mapped[DbColumnConstants.StandardNullableDecimal]

    price_per_ru: Mapped[DbColumnConstants.StandardNullableVarchar]
    price_per_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    price_per_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    average_training_time_in_minute: Mapped[DbColumnConstants.StandardNullableInteger]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    academy: Mapped[AppEntityNames.AcademyEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.AcademyEntityName,
        back_populates="academy_groups",
        foreign_keys=f"{AppEntityNames.AcademyGroupEntityName}.academy_id",
    )

    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="academy_groups",
        foreign_keys=f"{AppEntityNames.AcademyGroupEntityName}.image_id",
    )

    academy_group_schedules: Mapped[list[AppEntityNames.AcademyGroupScheduleEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGroupScheduleEntityName,
            back_populates="group",
            foreign_keys=f"{AppEntityNames.AcademyGroupScheduleEntityName}.group_id",
        )
    )

    academy_group_students: Mapped[list[AppEntityNames.AcademyGroupStudentEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGroupStudentEntityName,
            back_populates="group",
            foreign_keys=f"{AppEntityNames.AcademyGroupStudentEntityName}.group_id",
        )
    )

    academy_materials: Mapped[list[AppEntityNames.AcademyMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyMaterialEntityName,
            back_populates="group",
            foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.group_id",
        )
    )

    request_to_academy_groups: Mapped[list[AppEntityNames.RequestToAcademyGroupEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RequestToAcademyGroupEntityName,
            back_populates="group",
            foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.group_id",
        )
    )

    academy_galleries: Mapped[list[AppEntityNames.AcademyGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGalleryEntityName,
            back_populates="group",
            foreign_keys=f"{AppEntityNames.AcademyGalleryEntityName}.group_id",
        )
    )

