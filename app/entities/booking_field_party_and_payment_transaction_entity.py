from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class BookingFieldPartyAndPaymentTransactionEntity(Base):
    """
    Связующая таблица между BookingFieldPartyRequest и PaymentTransaction.

    Позволяет отслеживать связи многие-ко-многим между бронированиями площадок и платежными транзакциями.
    Это полезно для случаев, когда:
    - Одно бронирование может иметь несколько попыток оплаты (перевыставленные счета)
    - Одна транзакция может быть связана с несколькими бронированиями (групповая оплата)
    """
    __tablename__ = AppTableNames.BookingFieldPartyAndPaymentTransactionTableName

    id: Mapped[DbColumnConstants.ID]

    request_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.BookingFieldPartyRequestTableName,
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
    booking_request: Mapped[AppEntityNames.BookingFieldPartyRequestEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.BookingFieldPartyRequestEntityName,
        back_populates="payment_transactions",
        lazy="select",
    )

    payment_transaction: Mapped[AppEntityNames.PaymentTransactionEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.PaymentTransactionEntityName,
        foreign_keys=f"{AppEntityNames.BookingFieldPartyAndPaymentTransactionEntityName}.payment_transaction_id",
        lazy="select",
    )
