from sqlalchemy.orm import Mapped
from typing import Optional

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderItemHistoryEntity(Base):
    __tablename__ = AppTableNames.ProductOrderItemHistoryTableName
    id: Mapped[DbColumnConstants.ID]
    order_item_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductOrderItemTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderItemStatusTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    responsible_user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    message_ru: Mapped[DbColumnConstants.StandardNullableVarchar]
    message_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    message_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    is_passed: Mapped[DbColumnConstants.StandardBooleanNullable]
    cancel_reason: Mapped[DbColumnConstants.StandardNullableText]
    taken_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    passed_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    order_item: Mapped[AppEntityNames.ProductOrderItemEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderItemEntityName,
        back_populates="history_records",
        lazy="select",
    )

    status: Mapped[Optional[AppEntityNames.ProductOrderItemStatusEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderItemStatusEntityName,
        back_populates="history_records",
        lazy="select",
    )

    responsible_user: Mapped[Optional[AppEntityNames.UserEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemHistoryEntityName}.responsible_user_id",
        lazy="select",
    )