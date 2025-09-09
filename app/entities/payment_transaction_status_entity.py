from sqlalchemy.orm import Mapped, relationship
from typing import Optional

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class PaymentTransactionStatusEntity(Base):
    __tablename__ = AppTableNames.PaymentTransactionStatusTableName
    id: Mapped[DbColumnConstants.ID]
    previous_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    next_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionStatusTableName,
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
    previous_status: Mapped[Optional[AppEntityNames.PaymentTransactionStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.PaymentTransactionStatusEntityName,
            foreign_keys=f"{AppEntityNames.PaymentTransactionStatusEntityName}.previous_id",
            remote_side=f"{AppEntityNames.PaymentTransactionStatusEntityName}.id",
        )
    )

    next_status: Mapped[Optional[AppEntityNames.PaymentTransactionStatusEntityName]] = (
        DbRelationshipConstants.self_referential(
            target=AppEntityNames.PaymentTransactionStatusEntityName,
            foreign_keys=f"{AppEntityNames.PaymentTransactionStatusEntityName}.next_id",
            remote_side=f"{AppEntityNames.PaymentTransactionStatusEntityName}.id",
        )
    )
    
    # Relationship to PaymentTransactionEntity (one-to-many)
    payment_transactions: Mapped[list[AppEntityNames.PaymentTransactionEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.PaymentTransactionEntityName,
            back_populates="status",
            foreign_keys=f"{AppEntityNames.PaymentTransactionEntityName}.status_id",
            cascade="all, delete-orphan"
        )
    )

