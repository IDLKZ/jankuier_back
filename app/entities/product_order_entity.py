from sqlalchemy.orm import Mapped
from typing import Optional

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderEntity(Base):
    __tablename__ = AppTableNames.ProductOrderTableName
    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderStatusTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    canceled_by_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    payment_transaction_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PaymentTransactionsTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    shipping_total_price:Mapped[DbColumnConstants.StandardZeroDecimal]
    taxes_price:Mapped[DbColumnConstants.StandardZeroDecimal]
    total_price: Mapped[DbColumnConstants.StandardPrice]
    refunded_total: Mapped[DbColumnConstants.StandardZeroDecimal]
    order_items: Mapped[
        DbColumnConstants.StandardJSONB
    ]  # хранение snapshot товаров
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_refunded: Mapped[DbColumnConstants.StandardBooleanFalse]
    cancel_reason:Mapped[DbColumnConstants.StandardNullableText]
    cancel_refund_reason:Mapped[DbColumnConstants.StandardNullableText]
    email:Mapped[DbColumnConstants.StandardNullableVarchar]
    phone:Mapped[DbColumnConstants.StandardNullableVarchar]
    paid_until:Mapped[DbColumnConstants.StandardNullableDateTime]
    paid_at:Mapped[DbColumnConstants.StandardNullableDateTime]
    paid_order:Mapped[DbColumnConstants.StandardNullableVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderEntityName}.user_id",
        lazy="select",
    )

    canceled_by: Mapped[Optional[AppEntityNames.UserEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderEntityName}.canceled_by_id",
        lazy="select",
    )

    status: Mapped[Optional[AppEntityNames.ProductOrderStatusEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderStatusEntityName,
        back_populates="orders",
        lazy="select",
    )

    payment_transaction: Mapped[Optional[AppEntityNames.PaymentTransactionEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.PaymentTransactionEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderEntityName}.payment_transaction_id",
        lazy="select",
    )

    order_items: Mapped[list[AppEntityNames.ProductOrderItemEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderItemEntityName,
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="select",
    )

    payment_transactions: Mapped[list[AppEntityNames.ProductOrderAndPaymentTransactionEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderAndPaymentTransactionEntityName,
        back_populates="product_order",
        cascade="all, delete-orphan",
        lazy="select",
    )