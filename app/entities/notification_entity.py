from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class NotificationEntity(Base):
    __tablename__ = AppTableNames.NotificationTableName
    id: Mapped[DbColumnConstants.ID]
    topic_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.TopicNotificationTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    user_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.UserTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    topics: Mapped[DbColumnConstants.StandardNullableVarchar]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    description_ru: Mapped[DbColumnConstants.StandardText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]
    action_url: Mapped[DbColumnConstants.StandardNullableVarchar]
    inner_action_url: Mapped[DbColumnConstants.StandardNullableVarchar]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    topic: Mapped[AppEntityNames.TopicNotificationEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.TopicNotificationEntityName,
            back_populates="notifications",
            foreign_keys=f"{AppEntityNames.NotificationEntityName}.topic_id",
        )
    )

    user: Mapped[AppEntityNames.UserEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.UserEntityName,
        back_populates="notifications",
        foreign_keys=f"{AppEntityNames.NotificationEntityName}.user_id",
    )

    read_notifications: Mapped[list[AppEntityNames.ReadNotificationEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ReadNotificationEntityName,
            back_populates="notification",
            foreign_keys=f"{AppEntityNames.ReadNotificationEntityName}.notification_id",
        )
    )