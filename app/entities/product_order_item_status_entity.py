from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderItemStatusEntity(Base):
    __tablename__ = AppTableNames.ProductOrderItemStatusTableName
    id: Mapped[DbColumnConstants.ID]
    previous_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderItemStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderItemStatusTableName,
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
    previous_allowed_values: Mapped[DbColumnConstants.StandardArrayStringNullable]
    next_allowed_values: Mapped[DbColumnConstants.StandardArrayStringNullable]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    # Self-referencing relationships for status chain (using DbRelationshipConstants.self_referential)
    previous_status: Mapped[Optional[AppEntityNames.ProductOrderItemStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.ProductOrderItemStatusEntityName,
            foreign_keys=f"{AppEntityNames.ProductOrderItemStatusEntityName}.previous_id",
            remote_side=f"{AppEntityNames.ProductOrderItemStatusEntityName}.id",
        )
    )

    next_status: Mapped[Optional[AppEntityNames.ProductOrderItemStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.ProductOrderItemStatusEntityName,
            foreign_keys=f"{AppEntityNames.ProductOrderItemStatusEntityName}.next_id",
            remote_side=f"{AppEntityNames.ProductOrderItemStatusEntityName}.id",
        )
    )

    # Relationships to other entities
    order_items: Mapped[list[AppEntityNames.ProductOrderItemEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderItemEntityName,
        back_populates="status",
        lazy="select",
    )

    history_records: Mapped[list[AppEntityNames.ProductOrderItemHistoryEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderItemHistoryEntityName,
        back_populates="status",
        lazy="select",
    )