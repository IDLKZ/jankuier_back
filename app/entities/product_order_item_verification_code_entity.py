from sqlalchemy.orm import Mapped
from typing import Optional

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderItemVerificationCodeEntity(Base):
    __tablename__ = AppTableNames.ProductOrderItemVerificationCodeTableName
    id: Mapped[DbColumnConstants.ID]
    order_item_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductOrderItemTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    responsible_user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    code: Mapped[DbColumnConstants.StandardVarcharIndex]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    order_item: Mapped[AppEntityNames.ProductOrderItemEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderItemEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemVerificationCodeEntityName}.order_item_id",
        lazy="select",
    )

    responsible_user: Mapped[Optional[AppEntityNames.UserEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemVerificationCodeEntityName}.responsible_user_id",
        lazy="select",
    )