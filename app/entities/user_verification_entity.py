from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class UserVerificationEntity(Base):
    __tablename__ = AppTableNames.UserVerificationTableName

    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    sent_to: Mapped[DbColumnConstants.StandardText]
    code: Mapped[DbColumnConstants.StandardVarchar]
    active_until: Mapped[DbColumnConstants.StandardDateTime]
    used_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_used: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="verifications",
        foreign_keys=f"{AppEntityNames.UserVerificationEntityName}.user_id",
    )
