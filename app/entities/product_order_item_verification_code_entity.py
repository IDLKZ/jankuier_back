from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants
from app.shared.db_table_constants import AppTableNames


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
    code:Mapped[DbColumnConstants.StandardVarcharIndex]
    is_active:Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]