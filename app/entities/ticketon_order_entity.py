from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class TicketonOrderEntity(Base):
    __tablename__ = AppTableNames.TicketonOrderTableName
    id: Mapped[DbColumnConstants.ID]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.TicketonOrderStatusTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    payment_transaction_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionsTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    show: Mapped[DbColumnConstants.StandardVarcharIndex]
    show_info:Mapped[DbColumnConstants.StandardJSONB]
    seats: Mapped[DbColumnConstants.StandardArrayStringNullable]
    lang:Mapped[DbColumnConstants.StandardVarchar]
    pre_sale:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    sale:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    reservation_id:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    price:Mapped[DbColumnConstants.StandardNullablePrice]
    expire:Mapped[DbColumnConstants.StandardNullableInteger]
    expired_at:Mapped[DbColumnConstants.StandardNullableDateTime]
    sum:Mapped[DbColumnConstants.StandardNullablePrice]
    currency:Mapped[DbColumnConstants.StandardNullableVarchar]
    pre_tickets:Mapped[DbColumnConstants.StandardNullableJSONB]
    tickets:Mapped[DbColumnConstants.StandardNullableJSONB]
    sale_secury_token:Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    is_active:Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid:Mapped[DbColumnConstants.StandardBooleanFalse]
    is_canceled:Mapped[DbColumnConstants.StandardBooleanFalse]
    cancel_reason:Mapped[DbColumnConstants.StandardNullableVarchar]
    email:Mapped[DbColumnConstants.StandardNullableVarchar]
    phone:Mapped[DbColumnConstants.StandardNullableVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships (using DbRelationshipConstants)
    # Relationship to TicketonOrderStatusEntity (many-to-one)
    status: Mapped["TicketonOrderStatusEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="TicketonOrderStatusEntity",
            back_populates="ticketon_orders",
            foreign_keys="TicketonOrderEntity.status_id",
            cascade="none"
        )
    )
    
    # Relationship to UserEntity (many-to-one)
    user: Mapped["UserEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="UserEntity",
            back_populates="ticketon_orders",
            foreign_keys="TicketonOrderEntity.user_id",
            cascade="none"
        )
    )
    
    # Relationship to PaymentTransactionEntity (many-to-one)
    payment_transaction: Mapped["PaymentTransactionEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="PaymentTransactionEntity",
            back_populates="ticketon_orders",
            foreign_keys="TicketonOrderEntity.payment_transaction_id",
            cascade="none"
        )
    )


