from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class CountryEntity(Base):
    __tablename__ = AppTableNames.CountryTableName
    id: Mapped[DbColumnConstants.ID]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    sota_code: Mapped[DbColumnConstants.StandardNullableVarcharIndex]
    sota_flag_image: Mapped[DbColumnConstants.StandardNullableText]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    # Relationships
    cities: Mapped[list[AppEntityNames.CityEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.CityEntityName,
            back_populates="country",
            foreign_keys=f"{AppEntityNames.CityEntityName}.country_id",
        )
    )