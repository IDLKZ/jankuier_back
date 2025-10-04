from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class ReadNotificationEntity(Base):
    __tablename__ = AppTableNames.ReadNotificationTableName
    id: Mapped[DbColumnConstants.ID]
    notification_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.NotificationTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    notification: Mapped[AppEntityNames.NotificationEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.NotificationEntityName,
            back_populates="read_notifications",
            foreign_keys=f"{AppEntityNames.ReadNotificationEntityName}.notification_id",
        )
    )

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="read_notifications",
        foreign_keys=f"{AppEntityNames.ReadNotificationEntityName}.user_id",
    )