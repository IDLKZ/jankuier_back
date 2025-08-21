from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FieldPartyScheduleSettingsEntity(Base):
    __tablename__ = AppTableNames.FieldPartyScheduleSettingsTableName

    id: Mapped[DbColumnConstants.ID]

    party_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FieldPartyTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    active_start_at: Mapped[DbColumnConstants.StandardDate]
    active_end_at: Mapped[DbColumnConstants.StandardDate]

    # JSON поля
    working_days: Mapped[DbColumnConstants.StandardArrayInteger]  # [1,2,3,4,5]
    excluded_dates: Mapped[
        DbColumnConstants.StandardNullableArrayDate
    ]  # ["2025-10-10","2025-10-20"]
    working_time: Mapped[
        DbColumnConstants.StandardJSONB
    ]  # [{"start":"09:00","end":"18:00"}]
    break_time: Mapped[
        DbColumnConstants.StandardJSONB
    ]  # [{"start":"12:00","end":"13:00"}]
    price_per_time: Mapped[
        DbColumnConstants.StandardJSONB
    ]  # [{"start":"09:00","end":"12:00","price":15000}]

    session_minute_int: Mapped[DbColumnConstants.StandardInteger]
    break_between_session_int: Mapped[DbColumnConstants.StandardInteger]
    booked_limit: Mapped[DbColumnConstants.StandardInteger]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    party: Mapped[AppEntityNames.FieldPartyEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.FieldPartyEntityName,
            back_populates="field_party_schedule_settings",
            foreign_keys=f"{AppEntityNames.FieldPartyScheduleSettingsEntityName}.party_id",
        )
    )

    field_party_schedules: Mapped[list[AppEntityNames.FieldPartyScheduleEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldPartyScheduleEntityName,
            back_populates="setting",
            foreign_keys=f"{AppEntityNames.FieldPartyScheduleEntityName}.setting_id",
        )
    )
