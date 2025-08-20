from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class RoleEntity(Base):
    __tablename__ = AppTableNames.RoleTableName
    id: Mapped[DbColumnConstants.ID]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    description_ru: Mapped[DbColumnConstants.StandardNullableText]
    description_kk: Mapped[DbColumnConstants.StandardNullableText]
    description_en: Mapped[DbColumnConstants.StandardNullableText]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    is_active: Mapped[DbColumnConstants.StandardBooleanTrue]
    can_register: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_system: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_administrative: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    role_permissions: Mapped[list[AppEntityNames.RolePermissionEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RolePermissionEntityName,
            back_populates="role",
            foreign_keys=f"{AppEntityNames.RolePermissionEntityName}.role_id",
            overlaps="permissions",
        )
    )

    permissions: Mapped[list[AppEntityNames.PermissionEntityName]] = (
        DbRelationshipConstants.many_to_many(
            target=AppEntityNames.PermissionEntityName,
            secondary=AppTableNames.RolePermissionTableName,
            back_populates="roles",
            overlaps="role_permissions",
        )
    )

    users: Mapped[list[AppEntityNames.UserEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.UserEntityName,
            back_populates="role",
            foreign_keys=f"{AppEntityNames.UserEntityName}.role_id",
        )
    )
