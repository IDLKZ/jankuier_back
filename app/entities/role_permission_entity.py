from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class RolePermissionEntity(Base):
    __tablename__ = AppTableNames.RolePermissionTableName
    id: Mapped[DbColumnConstants.ID]
    role_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.RoleTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    permission_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.PermissionTableName,
            onupdate="CASCADE",
            ondelete="CASCADE",
        )
    ]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    role: Mapped[AppEntityNames.RoleEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.RoleEntityName,
        back_populates="role_permissions",
        foreign_keys=f"{AppEntityNames.RolePermissionEntityName}.role_id",
        overlaps="permissions,roles",
    )

    permission: Mapped[AppEntityNames.PermissionEntityName] = (
        DbRelationshipConstants.many_to_one(
            target=AppEntityNames.PermissionEntityName,
            back_populates="role_permissions",
            foreign_keys=f"{AppEntityNames.RolePermissionEntityName}.permission_id",
            overlaps="permissions,roles",
        )
    )
