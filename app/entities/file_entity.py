from sqlalchemy.orm import Mapped

from app.infrastructure.db import Base
from app.shared.db_constants import DbColumnConstants, DbRelationshipConstants
from app.shared.db_table_constants import AppTableNames
from app.shared.entity_constants import AppEntityNames


class FileEntity(Base):
    __tablename__ = AppTableNames.FileTableName
    id: Mapped[DbColumnConstants.ID]
    filename: Mapped[DbColumnConstants.StandardVarchar]
    file_path: Mapped[DbColumnConstants.StandardText]
    file_size: Mapped[DbColumnConstants.StandardInteger]
    content_type: Mapped[DbColumnConstants.StandardVarchar]
    is_remote: Mapped[DbColumnConstants.StandardBooleanFalse]
    created_at: Mapped[DbColumnConstants.CreatedAt]
    updated_at: Mapped[DbColumnConstants.UpdatedAt]

    users: Mapped[list[AppEntityNames.UserEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.UserEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.UserEntityName}.image_id",
        )
    )

    products: Mapped[list[AppEntityNames.ProductEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.ProductEntityName}.image_id",
        )
    )

    academies: Mapped[list[AppEntityNames.AcademyEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.AcademyEntityName}.image_id",
        )
    )

    product_galleries: Mapped[list[AppEntityNames.ProductGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductGalleryEntityName,
            back_populates="file",
            foreign_keys=f"{AppEntityNames.ProductGalleryEntityName}.file_id",
        )
    )

    academy_galleries: Mapped[list[AppEntityNames.AcademyGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGalleryEntityName,
            back_populates="file",
            foreign_keys=f"{AppEntityNames.AcademyGalleryEntityName}.file_id",
        )
    )

    field_galleries: Mapped[list[AppEntityNames.FieldGalleryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldGalleryEntityName,
            back_populates="file",
            foreign_keys=f"{AppEntityNames.FieldGalleryEntityName}.file_id",
        )
    )

    product_categories: Mapped[list[AppEntityNames.ProductCategoryEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductCategoryEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.ProductCategoryEntityName}.image_id",
        )
    )

    students: Mapped[list[AppEntityNames.StudentEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.StudentEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.StudentEntityName}.image_id",
        )
    )

    product_variants: Mapped[list[AppEntityNames.ProductVariantEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.ProductVariantEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.ProductVariantEntityName}.image_id",
        )
    )

    fields: Mapped[list[AppEntityNames.FieldEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.FieldEntityName}.image_id",
        )
    )

    academy_groups: Mapped[list[AppEntityNames.AcademyGroupEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyGroupEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.AcademyGroupEntityName}.image_id",
        )
    )

    academy_materials: Mapped[list[AppEntityNames.AcademyMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.AcademyMaterialEntityName,
            back_populates="file",
            foreign_keys=f"{AppEntityNames.AcademyMaterialEntityName}.file_id",
        )
    )

    request_materials: Mapped[list[AppEntityNames.RequestMaterialEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.RequestMaterialEntityName,
            back_populates="file",
            foreign_keys=f"{AppEntityNames.RequestMaterialEntityName}.file_id",
        )
    )

    field_parties: Mapped[list[AppEntityNames.FieldPartyEntityName]] = (
        DbRelationshipConstants.one_to_many(
            target=AppEntityNames.FieldPartyEntityName,
            back_populates="image",
            foreign_keys=f"{AppEntityNames.FieldPartyEntityName}.image_id",
        )
    )

