from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FirebaseNotificationEntity(Base):
    __tablename__ = AppTableNames.FirebaseNotificationTableName
    id: Mapped[DbColumnConstants.ID]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    token: Mapped[DbColumnConstants.StandardText]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="firebase_notifications",
        foreign_keys=f"{AppEntityNames.FirebaseNotificationEntityName}.user_id",
    )