from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class PermissionEntity(Base):
    __tablename__ = AppTableNames.PermissionTableName
    id: Mapped[DbColumnConstants.ID]
    title_ru: Mapped[DbColumnConstants.StandardVarchar]
    title_kk: Mapped[DbColumnConstants.StandardNullableVarchar]
    title_en: Mapped[DbColumnConstants.StandardNullableVarchar]
    value: Mapped[DbColumnConstants.StandardUniqueValue]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    role_permissions: Mapped[list[AppEntityNames.RolePermissionEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RolePermissionEntityName,
            back_populates="permission",
            foreign_keys=f"{AppEntityNames.RolePermissionEntityName}.permission_id",
            overlaps="roles",
        )
    )

    roles: Mapped[list[AppEntityNames.RoleEntityName]] = (
        DbRelationshipConstants.many_to_many(
            target=AppEntityNames.RoleEntityName,
            secondary=AppTableNames.RolePermissionTableName,
            back_populates="permissions",
            overlaps="role_permissions",
        )
    )
