from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderAndPaymentTransactionEntity(Base):
    __tablename__ = AppTableNames.ProductOrderAndPaymentTransactionTableName

    id: Mapped[DbColumnConstants.ID]

    product_order_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductOrderTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    payment_transaction_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.PaymentTransactionsTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    # Статус связи
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_primary: Mapped[DbColumnConstants.StandardBooleanFalse]  # Основная транзакция для заказа

    # Метаинформация о связи
    link_type: Mapped[DbColumnConstants.StandardVarchar]  # 'initial', 'recreated', 'refund', etc.
    link_reason: Mapped[DbColumnConstants.StandardNullableText]  # Причина создания связи

    # Временные метки
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    product_order: Mapped[AppEntityNames.ProductOrderEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderEntityName,
        back_populates="payment_transactions",
        lazy="select",
    )

    payment_transaction: Mapped[AppEntityNames.PaymentTransactionEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.PaymentTransactionEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderAndPaymentTransactionEntityName}.payment_transaction_id",
        lazy="select",
    )