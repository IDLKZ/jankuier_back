from app.entities.academy_entity import AcademyEntity
from app.entities.academy_gallery_entity import AcademyGalleryEntity
from app.entities.academy_group_entity import AcademyGroupEntity
from app.entities.academy_group_schedule_entity import AcademyGroupScheduleEntity
from app.entities.academy_group_student_entity import AcademyGroupStudentEntity
from app.entities.academy_material_entity import AcademyMaterialEntity
from app.entities.cart_entity import CartEntity
from app.entities.cart_item_entity import CartItemEntity
from app.entities.category_modification_entity import CategoryModificationEntity
from app.entities.city_entity import CityEntity
from app.entities.country_entity import CountryEntity
from app.entities.field_entity import FieldEntity
from app.entities.field_gallery_entity import FieldGalleryEntity
from app.entities.field_party_entity import FieldPartyEntity
from app.entities.field_party_schedule_entity import FieldPartyScheduleEntity
from app.entities.field_party_schedule_settings_entity import (
    FieldPartyScheduleSettingsEntity,
)
from app.entities.file_entity import FileEntity
from app.entities.modification_type_entity import ModificationTypeEntity
from app.entities.modification_value_entity import ModificationValueEntity
from app.entities.permission_entity import PermissionEntity
from app.entities.product_category_entity import ProductCategoryEntity
from app.entities.product_entity import ProductEntity
from app.entities.product_gallery_entity import ProductGalleryEntity
from app.entities.product_variant_entity import ProductVariantEntity
from app.entities.product_variant_modification_entity import (
    ProductVariantModificationEntity,
)
from app.entities.request_material_entity import RequestMaterialEntity
from app.entities.request_to_academy_group_entity import RequestToAcademyGroupEntity
from app.entities.role_entity import RoleEntity
from app.entities.role_permission_entity import RolePermissionEntity
from app.entities.sport_entity import SportEntity
from app.entities.student_entity import StudentEntity
from app.entities.user_entity import UserEntity


__all__ = [
    FileEntity.__name__,
    CountryEntity.__name__,
    CityEntity.__name__,
    SportEntity.__name__,
    RoleEntity.__name__,
    PermissionEntity.__name__,
    RolePermissionEntity.__name__,
    UserEntity.__name__,
    ProductCategoryEntity.__name__,
    ProductEntity.__name__,
    ModificationTypeEntity.__name__,
    ProductVariantEntity.__name__,
    ModificationValueEntity.__name__,
    ProductVariantModificationEntity.__name__,
    CategoryModificationEntity.__name__,
    ProductGalleryEntity.__name__,
    FieldEntity.__name__,
    FieldPartyEntity.__name__,
    FieldPartyScheduleSettingsEntity.__name__,
    FieldPartyScheduleEntity.__name__,
    FieldGalleryEntity.__name__,
    AcademyEntity.__name__,
    AcademyGroupEntity.__name__,
    AcademyGroupScheduleEntity.__name__,
    AcademyGalleryEntity.__name__,
    AcademyMaterialEntity.__name__,
    StudentEntity.__name__,
    RequestToAcademyGroupEntity.__name__,
    RequestMaterialEntity.__name__,
    AcademyGroupStudentEntity.__name__,
    CartEntity.__name__,
    CartItemEntity.__name__,
]
