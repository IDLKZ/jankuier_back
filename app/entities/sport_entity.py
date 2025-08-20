from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants
from app.shared.db_table_constants import AppTableNames


class SportEntity(Base):
    __tablename__ = AppTableNames.SportTableName
    id: Mapped[DbColumnConstants.ID]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]