from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class PaymentTransactionEntity(Base):
    __tablename__ = AppTableNames.PaymentTransactionsTableName
    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    transaction_type:Mapped[DbColumnConstants.StandardVarcharIndex]
    order:Mapped[DbColumnConstants.StandardVarcharIndex]
    nonce:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    mpi_order:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    amount:Mapped[DbColumnConstants.StandardPrice]
    currency:Mapped[DbColumnConstants.StandardVarchar]
    merchant:Mapped[DbColumnConstants.StandardVarchar]
    language:Mapped[DbColumnConstants.StandardNullableVarchar]
    client_id:Mapped[DbColumnConstants.StandardNullableInteger]
    desc:Mapped[DbColumnConstants.StandardVarchar]
    desc_order:Mapped[DbColumnConstants.StandardNullableText]
    email:Mapped[DbColumnConstants.StandardNullableVarchar]
    backref:Mapped[DbColumnConstants.StandardNullableText]
    wtype:Mapped[DbColumnConstants.StandardNullableVarchar]
    name:Mapped[DbColumnConstants.StandardNullableVarchar]
    pre_p_sign:Mapped[DbColumnConstants.StandardNullableText]
    is_active: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    expired_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    res_code:Mapped[DbColumnConstants.StandardNullableVarchar]
    res_desc:Mapped[DbColumnConstants.StandardNullableText]
    paid_p_sign:Mapped[DbColumnConstants.StandardNullableText]
    rev_amount:Mapped[DbColumnConstants.StandardNullablePrice]
    rev_desc: Mapped[DbColumnConstants.StandardNullableText]
    cancel_p_sign:Mapped[DbColumnConstants.StandardNullableText]
    order_full_info:Mapped[DbColumnConstants.StandardNullableJSONB]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships (using DbRelationshipConstants)
    # Relationship to UserEntity (many-to-one)
    user: Mapped["UserEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="UserEntity",
            back_populates="payment_transactions",
            foreign_keys="PaymentTransactionEntity.user_id",
            cascade="none"
        )
    )
    
    # Relationship to PaymentTransactionStatusEntity (many-to-one)
    status: Mapped["PaymentTransactionStatusEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="PaymentTransactionStatusEntity",
            back_populates="payment_transactions",
            foreign_keys="PaymentTransactionEntity.status_id",
            cascade="none"
        )
    )
    
    # Relationship to TicketonOrderEntity (one-to-many)
    ticketon_orders: Mapped[list["TicketonOrderEntity"]] = (
        DbRelationshipConstants.one_to_many(
            target="TicketonOrderEntity",
            back_populates="payment_transaction",
            foreign_keys="TicketonOrderEntity.payment_transaction_id",
            cascade="all, delete-orphan"
        )
    )

    # Relationship to TicketonOrderAndPaymentTransactionEntity (one-to-many)
    ticketon_order_links: Mapped[list["TicketonOrderAndPaymentTransactionEntity"]] = (
        DbRelationshipConstants.one_to_many(
            target="TicketonOrderAndPaymentTransactionEntity",
            back_populates="payment_transaction",
            foreign_keys="TicketonOrderAndPaymentTransactionEntity.payment_transaction_id",
            cascade="all, delete-orphan"
        )
    )

