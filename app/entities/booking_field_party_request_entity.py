from typing import Optional

from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class BookingFieldPartyRequestEntity(Base):
    __tablename__ = AppTableNames.BookingFieldPartyRequestTableName
    id: Mapped[DbColumnConstants.ID]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.BookingFieldPartyStatusTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    field_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FieldTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    field_party_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FieldPartyTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    payment_transaction_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionsTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    total_price: Mapped[DbColumnConstants.StandardPrice]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_refunded: Mapped[DbColumnConstants.StandardBooleanFalse]
    cancel_reason: Mapped[DbColumnConstants.StandardNullableText]
    cancel_refund_reason: Mapped[DbColumnConstants.StandardNullableText]
    email: Mapped[DbColumnConstants.StandardNullableVarchar]
    phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    paid_until: Mapped[DbColumnConstants.StandardNullableDateTime]
    paid_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    paid_order: Mapped[DbColumnConstants.StandardNullableVarchar]
    start_at: Mapped[DbColumnConstants.StandardDateTime]
    end_at: Mapped[DbColumnConstants.StandardDateTime]
    reschedule_start_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    reschedule_end_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    status: Mapped[Optional[AppEntityNames.BookingFieldPartyStatusEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.BookingFieldPartyStatusEntityName,
        back_populates="booking_requests",
        lazy="select",
    )

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.BookingFieldPartyRequestEntityName}.user_id",
        lazy="select",
    )

    field: Mapped[Optional[AppEntityNames.FieldEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldEntityName,
        foreign_keys=f"{AppEntityNames.BookingFieldPartyRequestEntityName}.field_id",
        lazy="select",
    )

    field_party: Mapped[Optional[AppEntityNames.FieldPartyEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldPartyEntityName,
        foreign_keys=f"{AppEntityNames.BookingFieldPartyRequestEntityName}.field_party_id",
        lazy="select",
    )

    payment_transaction: Mapped[Optional[AppEntityNames.PaymentTransactionEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.PaymentTransactionEntityName,
        foreign_keys=f"{AppEntityNames.BookingFieldPartyRequestEntityName}.payment_transaction_id",
        lazy="select",
    )

    payment_transactions: Mapped[list[AppEntityNames.BookingFieldPartyAndPaymentTransactionEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.BookingFieldPartyAndPaymentTransactionEntityName,
        back_populates="booking_request",
        cascade="all, delete-orphan",
        lazy="select",
    )