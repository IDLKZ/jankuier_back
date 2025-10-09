from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class UserCodeResetPasswordEntity(Base):
    __tablename__ = AppTableNames.UserCodeResetPasswordTableName
    id: Mapped[DbColumnConstants.ID]
    user_id:Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    expired_at:Mapped[DbColumnConstants.StandardDateTime]
    code: Mapped[DbColumnConstants.StandardVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="user_code_reset_passwords",
        foreign_keys=f"{AppEntityNames.UserCodeResetPasswordEntityName}.user_id",
    )
