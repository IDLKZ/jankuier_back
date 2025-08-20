from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FieldEntity(Base):
    __tablename__ = AppTableNames.FieldTableName

    id: Mapped[DbColumnConstants.ID]

    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    city_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.CityTableName,
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

    value: Mapped[DbColumnConstants.StandardUniqueValue]

    address_ru: Mapped[DbColumnConstants.StandardNullableVarchar]
    address_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    address_kk: Mapped[DbColumnConstants.StandardNullableVarchar]

    latitude: Mapped[DbColumnConstants.StandardNullableVarchar]
    longitude: Mapped[DbColumnConstants.StandardNullableVarchar]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    has_cover: Mapped[DbColumnConstants.StandardBooleanFalse]

    phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    additional_phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardNullableVarchar]

    whatsapp: Mapped[DbColumnConstants.StandardNullableVarchar]
    telegram: Mapped[DbColumnConstants.StandardNullableVarchar]
    instagram: Mapped[DbColumnConstants.StandardNullableVarchar]
    tiktok: Mapped[DbColumnConstants.StandardNullableVarchar]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="fields",
        foreign_keys=f"{AppEntityNames.FieldEntityName}.image_id",
    )

    city: Mapped[AppEntityNames.CityEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        back_populates="fields",
        foreign_keys=f"{AppEntityNames.FieldEntityName}.city_id",
    )

    field_parties: Mapped[list[AppEntityNames.FieldPartyEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldPartyEntityName,
            back_populates="field",
            foreign_keys=f"{AppEntityNames.FieldPartyEntityName}.field_id",
        )
    )

    field_galleries: Mapped[list[AppEntityNames.FieldGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldGalleryEntityName,
            back_populates="field",
            foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.field_id",
        )
    )
