from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames


class TicketonOrderAndPaymentTransactionEntity(Base):
    """
    Связующая таблица между TicketonOrder и PaymentTransaction.

    Позволяет отслеживать связи многие-ко-многим между заказами Ticketon и платежными транзакциями.
    Это полезно для случаев, когда:
    - Один заказ может иметь несколько попыток оплаты (перевыставленные счета)
    - Одна транзакция может быть связана с несколькими заказами (групповая оплата)
    """
    __tablename__ = AppTableNames.TicketonOrderAndPaymentTransactionTableName

    id: Mapped[DbColumnConstants.ID]

    ticketon_order_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.TicketonOrderTableName,
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
    # Relationship to TicketonOrderEntity (many-to-one)
    ticketon_order: Mapped["TicketonOrderEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="TicketonOrderEntity",
            back_populates="payment_transaction_links",
            foreign_keys="TicketonOrderAndPaymentTransactionEntity.ticketon_order_id",
            cascade="none"
        )
    )

    # Relationship to PaymentTransactionEntity (many-to-one)
    payment_transaction: Mapped["PaymentTransactionEntity"] = (
        DbRelationshipConstants.many_to_one(
            target="PaymentTransactionEntity",
            back_populates="ticketon_order_links",
            foreign_keys="TicketonOrderAndPaymentTransactionEntity.payment_transaction_id",
            cascade="none"
        )
    )