from sqlalchemy.orm import Mapped

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
