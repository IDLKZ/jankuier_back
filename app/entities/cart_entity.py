from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class CartEntity(Base):
    __tablename__ = AppTableNames.CartTableName
    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    total_price: Mapped[DbColumnConstants.StandardZeroDecimal]
    cart_items: Mapped[
        DbColumnConstants.StandardNullableJSONB
    ]  # хранение snapshot товаров
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="carts",
        foreign_keys=f"{AppEntityNames.CartEntityName}.user_id",
    )

    cart_items_list: Mapped[list[AppEntityNames.CartItemEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.CartItemEntityName,
            back_populates="cart",
            foreign_keys=f"{AppEntityNames.CartItemEntityName}.cart_id",
            cascade="all, delete",
        )
    )
