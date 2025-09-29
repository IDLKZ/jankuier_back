from sqlalchemy.orm import Mapped
from typing import Optional

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants, app_db_computed
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ProductOrderItemEntity(Base):
    __tablename__ = AppTableNames.ProductOrderItemTableName
    id: Mapped[DbColumnConstants.ID]
    order_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductOrderTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    status_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductOrderItemStatusTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    canceled_by_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    product_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.ProductTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    variant_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.ProductVariantTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    from_city_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.CityTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    to_city_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.CityTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    qty: Mapped[DbColumnConstants.StandardInteger]
    sku: Mapped[DbColumnConstants.StandardNullableVarchar]
    product_price: Mapped[DbColumnConstants.StandardPrice]
    delta_price: Mapped[DbColumnConstants.StandardZeroDecimal]
    shipping_price: Mapped[DbColumnConstants.StandardZeroDecimal]
    unit_price: Mapped[
        DbColumnConstants.StandardComputedDecimal(
            table_exp=app_db_computed.count_unit_with_shipping_price, is_persisted=True
        )
    ]
    total_price: Mapped[
        DbColumnConstants.StandardComputedDecimal(
            table_exp=app_db_computed.count_price_with_qty_with_shipping_price, is_persisted=True
        )
    ]  # unit_price
    refunded_total: Mapped[DbColumnConstants.StandardZeroDecimal]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_canceled: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_paid: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_refunded: Mapped[DbColumnConstants.StandardBooleanFalse]
    cancel_reason:Mapped[DbColumnConstants.StandardNullableText]
    cancel_refund_reason:Mapped[DbColumnConstants.StandardNullableText]
    delivery_date: Mapped[DbColumnConstants.StandardNullableDateTime]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    order: Mapped[AppEntityNames.ProductOrderEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderEntityName,
        back_populates="order_items",
        lazy="select",
    )

    status: Mapped[Optional[AppEntityNames.ProductOrderItemStatusEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductOrderItemStatusEntityName,
        back_populates="order_items",
        lazy="select",
    )

    canceled_by: Mapped[Optional[AppEntityNames.UserEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemEntityName}.canceled_by_id",
        lazy="select",
    )

    product: Mapped[AppEntityNames.ProductEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemEntityName}.product_id",
        lazy="select",
    )

    variant: Mapped[Optional[AppEntityNames.ProductVariantEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.ProductVariantEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemEntityName}.variant_id",
        lazy="select",
    )

    from_city: Mapped[AppEntityNames.CityEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemEntityName}.from_city_id",
        lazy="select",
    )

    to_city: Mapped[Optional[AppEntityNames.CityEntityName]] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        foreign_keys=f"{AppEntityNames.ProductOrderItemEntityName}.to_city_id",
        lazy="select",
    )

    history_records: Mapped[list[AppEntityNames.ProductOrderItemHistoryEntityName]] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.ProductOrderItemHistoryEntityName,
        back_populates="order_item",
        cascade="all, delete-orphan",
        lazy="select",
    )