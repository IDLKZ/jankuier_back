from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FieldPartyScheduleEntity(Base):
    __tablename__ = AppTableNames.FieldPartyScheduleTableName

    id: Mapped[DbColumnConstants.ID]

    party_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FieldPartyTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    setting_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FieldPartyScheduleSettingsTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    day: Mapped[DbColumnConstants.StandardDate]
    start_at: Mapped[DbColumnConstants.StandardTime]
    end_at: Mapped[DbColumnConstants.StandardTime]

    price: Mapped[DbColumnConstants.StandardPrice]

    is_booked: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    party: Mapped[AppEntityNames.FieldPartyEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldPartyEntityName,
        back_populates="field_party_schedules",
        foreign_keys=f"{AppEntityNames.FieldPartyScheduleEntityName}.party_id",
    )

    setting: Mapped[AppEntityNames.FieldPartyScheduleSettingsEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldPartyScheduleSettingsEntityName,
        back_populates="field_party_schedules",
        foreign_keys=f"{AppEntityNames.FieldPartyScheduleEntityName}.setting_id",
    )

