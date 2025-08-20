from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class AcademyEntity(Base):
    __tablename__ = AppTableNames.AcademyTableName

    id: Mapped[DbColumnConstants.ID]

    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName, onupdate="CASCADE", ondelete="SET NULL"
        )
    ]
    city_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.CityTableName, onupdate="CASCADE", ondelete="SET NULL"
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
    address_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    address_en: Mapped[DbColumnConstants.StandardNullableVarchar]

    working_time: Mapped[DbColumnConstants.StandardJSONB]

    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]

    gender: Mapped[DbColumnConstants.StandardTinyInteger]  # 0 both, 1 male, 2 female
    min_age: Mapped[DbColumnConstants.StandardInteger]
    max_age: Mapped[DbColumnConstants.StandardInteger]

    average_price: Mapped[DbColumnConstants.StandardNullableDecimal]
    average_training_time_in_minute: Mapped[DbColumnConstants.StandardNullableInteger]

    phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    additional_phone: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardNullableVarchar]

    whatsapp: Mapped[DbColumnConstants.StandardNullableVarchar]
    telegram: Mapped[DbColumnConstants.StandardNullableVarchar]
    instagram: Mapped[DbColumnConstants.StandardNullableVarchar]
    tik_tok: Mapped[DbColumnConstants.StandardNullableVarchar]
    site: Mapped[DbColumnConstants.StandardNullableVarchar]

    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="academies",
        foreign_keys=f"{AppEntityNames.AcademyEntityName}.image_id",
    )

    city: Mapped[AppEntityNames.CityEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.CityEntityName,
        back_populates="academies",
        foreign_keys=f"{AppEntityNames.AcademyEntityName}.city_id",
    )

    academy_groups: Mapped[list[AppEntityNames.AcademyGroupEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGroupEntityName,
            back_populates="academy",
            foreign_keys=f"{AppEntityNames.AcademyGroupEntityName}.academy_id",
        )
    )

    academy_galleries: Mapped[list[AppEntityNames.AcademyGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGalleryEntityName,
            back_populates="academy",
            foreign_keys=f"{AppEntityNames.AcademyGalleryEntityName}.academy_id",
        )
    )

    academy_materials: Mapped[list[AppEntityNames.AcademyMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyMaterialEntityName,
            back_populates="academy",
            foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.academy_id",
        )
    )

