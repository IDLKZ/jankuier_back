from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class CartItemEntity(Base):
    __tablename__ = AppTableNames.CartItemTableName

    id: Mapped[DbColumnConstants.ID]

    cart_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.CartTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    product_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    variant_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductVariantTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]

    qty: Mapped[DbColumnConstants.StandardInteger]
    sku: Mapped[DbColumnConstants.StandardNullableVarchar]

    product_price: Mapped[DbColumnConstants.StandardPrice]
    delta_price: Mapped[DbColumnConstants.StandardZeroDecimal]

    unit_price: Mapped[DbColumnConstants.StandardDecimal]  # product_price + delta
    total_price: Mapped[DbColumnConstants.StandardDecimal]  # unit_price * qty

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    cart: Mapped[AppEntityNames.CartEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CartEntityName,
        back_populates="cart_items_list",
        foreign_keys=f"{AppEntityNames.CartItemEntityName}.cart_id",
    )

    product: Mapped[AppEntityNames.ProductEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductEntityName,
        back_populates="cart_items",
        foreign_keys=f"{AppEntityNames.CartItemEntityName}.product_id",
    )

    variant: Mapped[AppEntityNames.ProductVariantEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductVariantEntityName,
        back_populates="cart_items",
        foreign_keys=f"{AppEntityNames.CartItemEntityName}.variant_id",
    )

