from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class UserCodeVerificationEntity(Base):
    __tablename__ = AppTableNames.UserCodeVerificationTableName

    id: Mapped[DbColumnConstants.ID]
    user_id:Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    expired_at:Mapped[DbColumnConstants.StandardDateTime]
    code: Mapped[DbColumnConstants.StandardVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="user_code_verifications",
        foreign_keys=f"{AppEntityNames.UserCodeVerificationEntityName}.user_id",
    )
