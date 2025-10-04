from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class TopicNotificationEntity(Base):
    __tablename__ = AppTableNames.TopicNotificationTableName
    id: Mapped[DbColumnConstants.ID]
    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="topic_notifications",
        foreign_keys=f"{AppEntityNames.TopicNotificationEntityName}.image_id",
    )

    notifications: Mapped[list[AppEntityNames.NotificationEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.NotificationEntityName,
            back_populates="topic",
            foreign_keys=f"{AppEntityNames.NotificationEntityName}.topic_id",
        )
    )