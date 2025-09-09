from app.adapters.api.academy.academy_api import AcademyApi
from app.adapters.api.academy_gallery.academy_gallery_api import AcademyGalleryApi
from app.adapters.api.academy_material.academy_material_api import AcademyMaterialApi
from app.adapters.api.academy_group.academy_group_api import AcademyGroupApi
from app.adapters.api.academy_group_schedule.academy_group_schedule_api import (
    AcademyGroupScheduleApi,
)
from app.adapters.api.academy_group_student.academy_group_student_api import (
    AcademyGroupStudentApi,
)
from app.adapters.api.auth.auth_api import AuthApi
from app.adapters.api.category_modification.category_modification_api import (
    CategoryModificationApi,
)
from app.adapters.api.cart.cart_api import CartApi
from app.adapters.api.cart_item.cart_item_api import CartItemApi
from app.adapters.api.city.city_api import CityApi
from app.adapters.api.country.country_api import CountryApi
from app.adapters.api.field.field_api import FieldApi
from app.adapters.api.field_gallery.field_gallery_api import FieldGalleryApi
from app.adapters.api.field_party.field_party_api import FieldPartyApi
from app.adapters.api.field_party_schedule.field_party_schedule_api import (
    FieldPartyScheduleApi,
)
from app.adapters.api.field_party_schedule_settings.field_party_schedule_settings_api import (
    FieldPartyScheduleSettingsApi,
)
from app.adapters.api.modification_type.modification_type_api import ModificationTypeApi
from app.adapters.api.modification_value.modification_value_api import (
    ModificationValueApi,
)
from app.adapters.api.permission.permission_api import PermissionApi
from app.adapters.api.payment_transaction_status.payment_transaction_status_api import PaymentTransactionStatusApi
from app.adapters.api.payment_transaction.payment_transaction_api import PaymentTransactionApi
from app.adapters.api.ticketon_order_status.ticketon_order_status_api import TicketonOrderStatusApi
from app.adapters.api.ticketon_order.ticketon_order_api import TicketonOrderApi
from app.adapters.api.product.product_api import ProductApi
from app.adapters.api.product_category.product_category_api import ProductCategoryApi
from app.adapters.api.product_gallery.product_gallery_api import ProductGalleryApi
from app.adapters.api.product_variant.product_variant_api import ProductVariantApi
from app.adapters.api.product_variant_modification.product_variant_modification_api import (
    ProductVariantModificationApi,
)
from app.adapters.api.request_to_academy_group.request_to_academy_group_api import (
    RequestToAcademyGroupApi,
)
from app.adapters.api.request_material.request_material_api import RequestMaterialApi
from app.adapters.api.role.role_api import RoleApi
from app.adapters.api.sport.sport_api import SportApi
from app.adapters.api.student.student_api import StudentApi
from app.adapters.api.test.test_api import TestApi
from app.adapters.api.ticketon.ticketon_api import TicketonApi
from app.adapters.api.user.user_api import UserApi
from app.shared.route_constants import RoutePathConstants


def include_routers(app) -> None:
    # Academy routes
    app.include_router(
        AcademyApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy",
        tags=["Академии"],
    )
    
    app.include_router(
        AcademyGalleryApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy-gallery",
        tags=["Галерея академий"],
    )
    
    app.include_router(
        AcademyMaterialApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy-material",
        tags=["Материалы академий"],
    )
    
    app.include_router(
        AcademyGroupApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy-group",
        tags=["Группы академий"],
    )
    
    app.include_router(
        AcademyGroupScheduleApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy-group-schedule",
        tags=["Расписания групп академий"],
    )
    
    app.include_router(
        AcademyGroupStudentApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/academy-group-student",
        tags=["Студенты групп академий"],
    )
    
    # Category and modification routes
    app.include_router(
        CategoryModificationApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/category-modification",
        tags=["Модификации категорий"],
    )
    
    # Cart routes
    app.include_router(
        CartApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/cart",
        tags=["Корзины"],
    )
    
    app.include_router(
        CartItemApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/cart-item",
        tags=["Товары в корзине"],
    )
    
    # Location routes
    app.include_router(
        CityApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/city",
        tags=["Города"],
    )
    
    app.include_router(
        CountryApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/country",
        tags=["Страны"],
    )
    
    # Field routes
    app.include_router(
        FieldApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/field",
        tags=["Поля"],
    )
    
    app.include_router(
        FieldGalleryApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/field-gallery",
        tags=["Галерея полей"],
    )
    
    app.include_router(
        FieldPartyApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/field-party",
        tags=["Площадки полей"],
    )
    
    app.include_router(
        FieldPartyScheduleApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/field-party-schedule",
        tags=["Расписания площадок"],
    )
    
    app.include_router(
        FieldPartyScheduleSettingsApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/field-party-schedule-settings",
        tags=["Настройки расписания площадок"],
    )
    
    # Modification routes
    app.include_router(
        ModificationTypeApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/modification-type",
        tags=["Типы модификаций"],
    )
    
    app.include_router(
        ModificationValueApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/modification-value",
        tags=["Значения модификаций"],
    )
    
    # Product routes
    app.include_router(
        ProductApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/product",
        tags=["Товары"],
    )
    
    app.include_router(
        ProductCategoryApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/product-category",
        tags=["Категории товаров"],
    )
    
    app.include_router(
        ProductGalleryApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/product-gallery",
        tags=["Галерея товаров"],
    )
    
    app.include_router(
        ProductVariantApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/product-variant",
        tags=["Варианты товаров"],
    )
    
    app.include_router(
        ProductVariantModificationApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/product-variant-modification",
        tags=["Модификации вариантов товаров"],
    )
    
    # Request routes
    app.include_router(
        RequestToAcademyGroupApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/request-to-academy-group",
        tags=["Заявки в группы академий"],
    )
    
    app.include_router(
        RequestMaterialApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/request-material",
        tags=["Материалы заявок"],
    )
    
    # Sport and student routes
    app.include_router(
        SportApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/sport",
        tags=["Виды спорта"],
    )
    
    app.include_router(
        StudentApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/student",
        tags=["Студенты"],
    )
    
    # System routes (User, Role, Permission)
    app.include_router(
        RoleApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.RolePathName}",
        tags=[RoutePathConstants.RoleTagName],
    )
    app.include_router(
        PermissionApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.PermissionPathName}",
        tags=[RoutePathConstants.PermissionTagName],
    )
    app.include_router(
        UserApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.UserPathName}",
        tags=[RoutePathConstants.UserTagName],
    )
    app.include_router(
        PaymentTransactionStatusApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.PaymentTransactionStatusPathName}",
        tags=[RoutePathConstants.PaymentTransactionStatusTagName],
    )
    app.include_router(
        PaymentTransactionApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.PaymentTransactionPathName}",
        tags=[RoutePathConstants.PaymentTransactionTagName],
    )
    app.include_router(
        TicketonOrderStatusApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.TicketonOrderStatusPathName}",
        tags=[RoutePathConstants.TicketonOrderStatusTagName],
    )
    app.include_router(
        TicketonOrderApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.TicketonOrderPathName}",
        tags=[RoutePathConstants.TicketonOrderTagName],
    )
    app.include_router(
        TestApi().router,
        prefix=f"{RoutePathConstants.BasePathName}test",
        tags=["Тестовые роуты"],
    )
    app.include_router(
        AuthApi().router,
        prefix=f"{RoutePathConstants.BasePathName}{RoutePathConstants.AuthPathName}",
        tags=[RoutePathConstants.AuthTagName],
    )
    
    # External API integrations
    app.include_router(
        TicketonApi().router,
        prefix=f"{RoutePathConstants.BasePathName}/ticketon",
        tags=["Ticketon API"],
    )
