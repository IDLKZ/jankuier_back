from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class BookingFieldPartyStatusEntity(Base):
    __tablename__ = AppTableNames.BookingFieldPartyStatusTableName
    id: Mapped[DbColumnConstants.ID]
    previous_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.BookingFieldPartyStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.BookingFieldPartyStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    is_first: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_last: Mapped[DbColumnConstants.StandardBooleanFalse]
    previous_allowed_values: Mapped[DbColumnConstants.StandardArrayStringNullable]
    next_allowed_values: Mapped[DbColumnConstants.StandardArrayStringNullable]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    # Self-referencing relationships for status chain (using DbRelationshipConstants.self_referential)
    previous_status: Mapped[Optional[AppEntityNames.BookingFieldPartyStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.BookingFieldPartyStatusEntityName,
            foreign_keys=f"{AppEntityNames.BookingFieldPartyStatusEntityName}.previous_id",
            remote_side=f"{AppEntityNames.BookingFieldPartyStatusEntityName}.id",
        )
    )

    next_status: Mapped[Optional[AppEntityNames.BookingFieldPartyStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.BookingFieldPartyStatusEntityName,
            foreign_keys=f"{AppEntityNames.BookingFieldPartyStatusEntityName}.next_id",
            remote_side=f"{AppEntityNames.BookingFieldPartyStatusEntityName}.id",
        )
    )

    booking_requests: Mapped[list[AppEntityNames.BookingFieldPartyRequestEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.BookingFieldPartyRequestEntityName,
        back_populates="status",
        lazy="select",
    )