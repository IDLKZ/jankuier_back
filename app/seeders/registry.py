from app.seeders.city.city_seeder import CitySeeder
from app.seeders.country.country_seeder import CountrySeeder
from app.seeders.role.role_seeder import RoleSeeder
from app.seeders.sport.sport_seeder import SportSeeder
from app.seeders.user.user_seeder import UserSeeder
from app.seeders.product_category.product_category_seeder import ProductCategorySeeder
from app.seeders.product.product_seeder import ProductSeeder
from app.seeders.modification_type.modification_type_seeder import ModificationTypeSeeder
from app.seeders.product_variant.product_variant_seeder import ProductVariantSeeder
from app.seeders.modification_value.modification_value_seeder import ModificationValueSeeder
from app.seeders.product_variant_modification.product_variant_modification_seeder import ProductVariantModificationSeeder
from app.seeders.field.field_seeder import FieldSeeder
from app.seeders.field_party.field_party_seeder import FieldPartySeeder
from app.seeders.field_party_schedule_settings.field_party_schedule_settings_seeder import FieldPartyScheduleSettingsSeeder
from app.seeders.academy.academy_seeder import AcademySeeder
from app.seeders.academy_group.academy_group_seeder import AcademyGroupSeeder
from app.seeders.academy_group_schedule.academy_group_schedule_seeder import AcademyGroupScheduleSeeder
from app.seeders.payment_transaction_status.payment_transaction_status_seeder import PaymentTransactionStatusSeeder
from app.seeders.ticketon_order_status.ticketon_order_status_seeder import TicketonOrderStatusSeeder
from app.seeders.product_order_status.product_order_status_seeder import ProductOrderStatusSeeder
from app.seeders.product_order_item_status.product_order_item_status_seeder import ProductOrderItemStatusSeeder

seeders = [
    RoleSeeder(),
    PaymentTransactionStatusSeeder(),
    TicketonOrderStatusSeeder(),
    ProductOrderStatusSeeder(),
    ProductOrderItemStatusSeeder(),
    UserSeeder(),
    CountrySeeder(),
    SportSeeder(),
    CitySeeder(),
    ProductCategorySeeder(),
    ModificationTypeSeeder(),
    ProductSeeder(),
    ModificationValueSeeder(),
    ProductVariantSeeder(),
    ProductVariantModificationSeeder(),
    FieldSeeder(),
    FieldPartySeeder(),
    FieldPartyScheduleSettingsSeeder(),
    AcademySeeder(),
    AcademyGroupSeeder(),
    AcademyGroupScheduleSeeder(),
]
