from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class AcademyGroupScheduleEntity(Base):
    __tablename__ = AppTableNames.AcademyGroupScheduleTableName

    id: Mapped[DbColumnConstants.ID]

    group_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.AcademyGroupTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]

    training_date: Mapped[DbColumnConstants.StandardDate]
    start_at: Mapped[DbColumnConstants.StandardTime]
    end_at: Mapped[DbColumnConstants.StandardTime]

    reschedule_start_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    reschedule_end_at: Mapped[DbColumnConstants.StandardNullableDateTime]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_finished: Mapped[DbColumnConstants.StandardBooleanFalse]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    group: Mapped[AppEntityNames.AcademyGroupEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.AcademyGroupEntityName,
            back_populates="academy_group_schedules",
            foreign_keys=f"{AppEntityNames.AcademyGroupScheduleEntityName}.group_id",
        )
    )
