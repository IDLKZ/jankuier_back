from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class CityEntity(Base):
    __tablename__ = AppTableNames.CityTableName
    id: Mapped[DbColumnConstants.ID]
    country_id: Mapped[
        DbColumnConstants.ForeignKeyInteger(
            AppTableNames.CountryTableName, onupdate="CASCADE", ondelete="CASCADE"
        )
    ]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    ticketon_city_id: Mapped[DbColumnConstants.StandardNullableInteger]
    ticketon_tag: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    country: Mapped[AppEntityNames.CountryEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.CountryEntityName,
            back_populates="cities",
            foreign_keys=f"{AppEntityNames.CityEntityName}.country_id",
        )
    )

    academies: Mapped[list[AppEntityNames.AcademyEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyEntityName,
            back_populates="city",
            foreign_keys=f"{AppEntityNames.AcademyEntityName}.city_id",
        )
    )

    products: Mapped[list[AppEntityNames.ProductEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductEntityName,
            back_populates="city",
            foreign_keys=f"{AppEntityNames.ProductEntityName}.city_id",
        )
    )

    fields: Mapped[list[AppEntityNames.FieldEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldEntityName,
            back_populates="city",
            foreign_keys=f"{AppEntityNames.FieldEntityName}.city_id",
        )
    )

    product_variants: Mapped[list[AppEntityNames.ProductVariantEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductVariantEntityName,
            back_populates="city",
            foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.city_id",
        )
    )
