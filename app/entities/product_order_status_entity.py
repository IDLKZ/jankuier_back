from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderStatusEntity(Base):
    __tablename__ = AppTableNames.ProductOrderStatusTableName
    id: Mapped[DbColumnConstants.ID]
    previous_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderStatusTableName,
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
    previous_status: Mapped[Optional[AppEntityNames.ProductOrderStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.ProductOrderStatusEntityName,
            foreign_keys=f"{AppEntityNames.ProductOrderStatusEntityName}.previous_id",
            remote_side=f"{AppEntityNames.ProductOrderStatusEntityName}.id",
        )
    )

    next_status: Mapped[Optional[AppEntityNames.ProductOrderStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.ProductOrderStatusEntityName,
            foreign_keys=f"{AppEntityNames.ProductOrderStatusEntityName}.next_id",
            remote_side=f"{AppEntityNames.ProductOrderStatusEntityName}.id",
        )
    )

    # Relationships to other entities
    orders: Mapped[list[AppEntityNames.ProductOrderEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderEntityName,
        back_populates="status",
        lazy="select",
    )