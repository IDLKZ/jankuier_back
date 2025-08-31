from datetime import date
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FieldPartyEntity(Base):
    __tablename__ = AppTableNames.FieldPartyTableName

    id: Mapped[DbColumnConstants.ID]

    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]

    field_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.FieldTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]

    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    value: Mapped[DbColumnConstants.StandardUniqueValue]
    person_qty: Mapped[DbColumnConstants.StandardInteger]

    length_m: Mapped[DbColumnConstants.StandardInteger]
    width_m: Mapped[DbColumnConstants.StandardInteger]
    deepth_m: Mapped[DbColumnConstants.StandardNullableInteger]

    latitude: Mapped[DbColumnConstants.StandardNullableVarchar]
    longitude: Mapped[DbColumnConstants.StandardNullableVarchar]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    is_covered: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_default: Mapped[DbColumnConstants.StandardBooleanFalse]

    cover_type: Mapped[DbColumnConstants.StandardTinyInteger]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="field_parties",
        foreign_keys=f"{AppEntityNames.FieldPartyEntityName}.image_id",
    )

    field: Mapped[AppEntityNames.FieldEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FieldEntityName,
        back_populates="field_parties",
        foreign_keys=f"{AppEntityNames.FieldPartyEntityName}.field_id",
    )

    field_galleries: Mapped[list[AppEntityNames.FieldGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldGalleryEntityName,
            back_populates="party",
            foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.party_id",
        )
    )

    field_party_schedules: Mapped[list[AppEntityNames.FieldPartyScheduleEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldPartyScheduleEntityName,
            back_populates="party",
            foreign_keys=f"{AppEntityNames.FieldPartyScheduleEntityName}.party_id",
        )
    )

    field_party_schedule_settings: Mapped[
        list[AppEntityNames.FieldPartyScheduleSettingsEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.FieldPartyScheduleSettingsEntityName,
        back_populates="party",
        foreign_keys=f"{AppEntityNames.FieldPartyScheduleSettingsEntityName}.party_id",
    )

    @property
    def active_schedule_setting(self):
        """Возвращает активную настройку расписания или последнюю по дате"""
        if not self.field_party_schedule_settings:
            return None
        
        today = date.today()
        
        # Получаем только неудаленные настройки
        active_settings = [
            setting for setting in self.field_party_schedule_settings 
            if setting.deleted_at is None
        ]
        
        if not active_settings:
            return None
        
        # Сначала ищем активную настройку (текущая дата в диапазоне active_start_at - active_end_at)
        for setting in active_settings:
            if setting.active_start_at <= today <= setting.active_end_at:
                return setting
        
        # Если активной нет, возвращаем последнюю по created_at
        return max(active_settings, key=lambda x: x.created_at)
