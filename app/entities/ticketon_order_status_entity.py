from typing import Optional

from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class TicketonOrderStatusEntity(Base):
    __tablename__ = AppTableNames.TicketonOrderStatusTableName
    id: Mapped[DbColumnConstants.ID]
    previous_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.TicketonOrderStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.TicketonOrderStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    is_first: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_last: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    # Self-referencing relationships for status chain (using DbRelationshipConstants.self_referential)
    previous_status: Mapped[Optional[AppEntityNames.TicketonOrderStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.TicketonOrderStatusEntityName,
            foreign_keys=f"{AppEntityNames.TicketonOrderStatusEntityName}.previous_id",
            remote_side=f"{AppEntityNames.TicketonOrderStatusEntityName}.id",
        )
    )

    next_status: Mapped[Optional[AppEntityNames.TicketonOrderStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.TicketonOrderStatusEntityName,
            foreign_keys=f"{AppEntityNames.TicketonOrderStatusEntityName}.next_id",
            remote_side=f"{AppEntityNames.TicketonOrderStatusEntityName}.id",
        )
    )
    
    # Relationship to TicketonOrderEntity (one-to-many)
    ticketon_orders: Mapped[list[AppEntityNames.TicketonOrderEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.TicketonOrderEntityName,
            back_populates="status_rel",
            foreign_keys=f"{AppEntityNames.TicketonOrderEntityName}.status_id",
            cascade="all, delete-orphan"
        )
    )