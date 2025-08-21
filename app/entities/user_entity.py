from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class UserEntity(Base):
    __tablename__ = AppTableNames.UserTableName
    id: Mapped[DbColumnConstants.ID]
    role_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.RoleTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    image_id: Mapped[
        DbColumnConstants.ForeignKeyNullableInteger(
            AppTableNames.FileTableName,
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    ]
    first_name: Mapped[DbColumnConstants.StandardVarchar]
    last_name: Mapped[DbColumnConstants.StandardVarchar]
    patronomic: Mapped[DbColumnConstants.StandardNullableVarchar]
    email: Mapped[DbColumnConstants.StandardUniqueEmail]
    phone: Mapped[DbColumnConstants.StandardUniquePhone]
    username: Mapped[DbColumnConstants.StandardUniqueValue]
    sex: Mapped[DbColumnConstants.StandardTinyInteger]
    iin: Mapped[DbColumnConstants.StandardNullableVarchar]
    birthdate: Mapped[DbColumnConstants.StandardDate]
    password_hash: Mapped[DbColumnConstants.StandardNullableText]
    is_active: Mapped[DbColumnConstants.StandardBooleanFalse]
    is_verified: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]
    deleted_at: Mapped[DbColumnConstants.DeletedAt]

    role: Mapped[AppEntityNames.RoleEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.RoleEntityName,
        back_populates="users",
        foreign_keys=f"{AppEntityNames.UserEntityName}.role_id",
    )

    image: Mapped[AppEntityNames.FileEntityName] = DbRelationshipConstants.many_to_one(
        target=AppEntityNames.FileEntityName,
        back_populates="users",
        foreign_keys=f"{AppEntityNames.UserEntityName}.image_id",
    )

    carts: Mapped[list[AppEntityNames.CartEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.CartEntityName,
            back_populates="user",
            foreign_keys=f"{AppEntityNames.CartEntityName}.user_id",
        )
    )

    user_verifications: Mapped[list[AppEntityNames.UserVerificationEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.UserVerificationEntityName,
            back_populates="user",
            foreign_keys=f"{AppEntityNames.UserVerificationEntityName}.user_id",
        )
    )

    created_students: Mapped[list[AppEntityNames.StudentEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.StudentEntityName,
            back_populates="created_by_user",
            foreign_keys=f"{AppEntityNames.StudentEntityName}.created_by",
        )
    )

    checked_requests_to_academy_groups: Mapped[
        list[AppEntityNames.RequestToAcademyGroupEntityName]
    ] = DbRelationshipConstants.one_to_many(
        target=AppEntityNames.RequestToAcademyGroupEntityName,
        back_populates="checked_by_user",
        foreign_keys=f"{AppEntityNames.RequestToAcademyGroupEntityName}.checked_by",
    )
