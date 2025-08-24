from starlette_admin.contrib.sqla import Admin, ModelView

from app.entities import RoleEntity, FileEntity, CartItemEntity, CartEntity, AcademyGroupStudentEntity, \
    RequestMaterialEntity, RequestToAcademyGroupEntity, StudentEntity, AcademyMaterialEntity, AcademyGalleryEntity, \
    AcademyGroupScheduleEntity, AcademyGroupEntity, AcademyEntity, FieldGalleryEntity, FieldPartyScheduleEntity, \
    FieldPartyScheduleSettingsEntity, FieldPartyEntity, FieldEntity, ProductGalleryEntity, CategoryModificationEntity, \
    ProductVariantModificationEntity, ModificationValueEntity, ProductVariantEntity, ModificationTypeEntity, \
    ProductEntity, ProductCategoryEntity, UserVerificationEntity, RolePermissionEntity, PermissionEntity, SportEntity, \
    CityEntity, CountryEntity
from app.entities.user_entity import UserEntity
from app.infrastructure.db import engine_sync


def setup_admin_dashboard(app):
    # Create admin
    admin = Admin(engine_sync, title="Example: SQLAlchemy")
    # Add view
    admin.add_view(ModelView(FileEntity, icon="fas fa-list", label="Файлы"))
    admin.add_view(ModelView(CountryEntity, icon="fas fa-list", label="Страны"))
    admin.add_view(ModelView(CityEntity, icon="fas fa-list", label="Города"))
    admin.add_view(ModelView(SportEntity, icon="fas fa-list", label="Виды спорта"))
    admin.add_view(ModelView(RoleEntity, icon="fas fa-list", label="Роли"))
    admin.add_view(ModelView(PermissionEntity, icon="fas fa-list", label="Права"))
    admin.add_view(ModelView(RolePermissionEntity, icon="fas fa-list", label="Роли и права"))
    admin.add_view(ModelView(UserEntity, icon="fas fa-list", label="Пользователи"))
    admin.add_view(ModelView(UserVerificationEntity, icon="fas fa-list", label="Подтверждения"))
    admin.add_view(ModelView(ProductCategoryEntity, icon="fas fa-list", label="Категории товаров"))
    admin.add_view(ModelView(ProductEntity, icon="fas fa-list", label="Товары"))
    admin.add_view(ModelView(ModificationTypeEntity, icon="fas fa-list", label="Типы модификаций"))
    admin.add_view(ModelView(ProductVariantEntity, icon="fas fa-list", label="Варианты товаров"))
    admin.add_view(ModelView(ModificationValueEntity, icon="fas fa-list", label="Значения модификаций"))
    admin.add_view(ModelView(ProductVariantModificationEntity, icon="fas fa-list", label="Модификации вариантов"))
    admin.add_view(ModelView(CategoryModificationEntity, icon="fas fa-list", label="Модификации категорий"))
    admin.add_view(ModelView(ProductGalleryEntity, icon="fas fa-list", label="Галерея товаров"))
    admin.add_view(ModelView(FieldEntity, icon="fas fa-list", label="Поля"))
    admin.add_view(ModelView(FieldPartyEntity, icon="fas fa-list", label="События на поле"))
    admin.add_view(ModelView(FieldPartyScheduleSettingsEntity, icon="fas fa-list", label="Настройки расписания поля"))
    admin.add_view(ModelView(FieldPartyScheduleEntity, icon="fas fa-list", label="Расписание событий на поле"))
    admin.add_view(ModelView(FieldGalleryEntity, icon="fas fa-list", label="Галерея поля"))
    admin.add_view(ModelView(AcademyEntity, icon="fas fa-list", label="Академии"))
    admin.add_view(ModelView(AcademyGroupEntity, icon="fas fa-list", label="Группы академии"))
    admin.add_view(ModelView(AcademyGroupScheduleEntity, icon="fas fa-list", label="Расписание групп академии"))
    admin.add_view(ModelView(AcademyGalleryEntity, icon="fas fa-list", label="Галерея академии"))
    admin.add_view(ModelView(AcademyMaterialEntity, icon="fas fa-list", label="Материалы академии"))
    admin.add_view(ModelView(StudentEntity, icon="fas fa-list", label="Студенты"))
    admin.add_view(ModelView(RequestToAcademyGroupEntity, icon="fas fa-list", label="Заявки в группы академии"))
    admin.add_view(ModelView(RequestMaterialEntity, icon="fas fa-list", label="Запрошенные материалы"))
    admin.add_view(ModelView(AcademyGroupStudentEntity, icon="fas fa-list", label="Студенты групп"))
    admin.add_view(ModelView(CartEntity, icon="fas fa-list", label="Корзины"))
    admin.add_view(ModelView(CartItemEntity, icon="fas fa-list", label="Товары в корзине"))

    # Mount admin to your app
    admin.mount_to(app)