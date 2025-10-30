from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class YandexAfishaWidgetTicketEntity(Base):
    __tablename__ = AppTableNames.YandexAfishaWidgetTicketTableName

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
    description_ru: Mapped[DbColumnConstants.StandardNullableText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]
    address_ru: Mapped[DbColumnConstants.StandardNullableVarchar]
    address_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    address_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    stadium_ru: Mapped[DbColumnConstants.StandardNullableVarchar]
    stadium_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    stadium_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    start_at: Mapped[DbColumnConstants.StandardNullableDateTime]
    yandex_session_id: Mapped[DbColumnConstants.StandardText]
    yandex_widget_url: Mapped[DbColumnConstants.StandardNullableText]
    is_active: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.FileEntityName,
            back_populates="yandex_afisha_widget_tickets",
        )
    )