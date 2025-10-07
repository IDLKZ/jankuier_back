from app.routes.academy.academy_route import assign_academy_roles
from app.routes.academy_gallery.academy_gallery_route import assign_academy_gallery_roles
from app.routes.academy_group.academy_group_route import assign_academy_group_roles
from app.routes.academy_group_schedule.academy_group_schedule_route import assign_academy_group_schedule_roles
from app.routes.academy_group_student.academy_group_student_route import assign_academy_group_student_roles
from app.routes.academy_material.academy_material_route import assign_academy_material_roles
from app.routes.auth.auth_route import assign_auth_roles
from app.routes.booking_field_party_status.booking_field_party_status_route import assign_booking_field_party_status_roles
from app.routes.booking_field_party_request.booking_field_party_request_route import assign_booking_field_party_request_roles
from app.routes.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_route import assign_booking_field_party_and_payment_transaction_roles
from app.routes.cart.cart_route import assign_cart_roles
from app.routes.cart_item.cart_item_route import assign_cart_item_roles
from app.routes.category_modification.category_modification_route import assign_category_modification_roles
from app.routes.city.city_route import assign_city_roles
from app.routes.country.country_route import assign_country_roles
from app.routes.field.field_route import assign_field_roles
from app.routes.field_gallery.field_gallery_route import assign_field_gallery_roles
from app.routes.field_party.field_party_route import assign_field_party_roles
from app.routes.field_party_schedule.field_party_schedule_route import assign_field_party_schedule_roles
from app.routes.field_party_schedule_settings.field_party_schedule_settings_route import assign_field_party_schedule_settings_roles
from app.routes.modification_type.modification_type_route import assign_modification_type_roles
from app.routes.modification_value.modification_value_route import assign_modification_value_roles
from app.routes.payment_transaction_status.payment_transaction_status_route import assign_payment_transaction_status_roles
from app.routes.payment_transaction.payment_transaction_route import assign_payment_transaction_roles
from app.routes.permission.permission_route import assign_permission_roles
from app.routes.product.product_route import assign_product_roles
from app.routes.product_category.product_category_route import assign_product_category_roles
from app.routes.product_gallery.product_gallery_route import assign_product_gallery_roles
from app.routes.product_variant.product_variant_route import assign_product_variant_roles
from app.routes.product_variant_modification.product_variant_modification_route import assign_product_variant_modification_roles
from app.routes.product_order.product_order_route import assign_product_order_roles
from app.routes.product_order_admin.product_order_admin_route import assign_product_order_admin_roles
from app.routes.product_order_item_admin.product_order_item_admin_route import assign_product_order_item_admin_roles
from app.routes.product_order_status.product_order_status_route import assign_product_order_status_roles
from app.routes.product_order_item_status.product_order_item_status_route import assign_product_order_item_status_roles
from app.routes.request_material.request_material_route import assign_request_material_roles
from app.routes.request_to_academy_group.request_to_academy_group_route import assign_request_to_academy_group_roles
from app.routes.role.role_route import assign_role_roles
from app.routes.sota.sota_route import assign_sota_roles
from app.routes.sport.sport_route import assign_sport_roles
from app.routes.student.student_route import assign_student_roles
from app.routes.test.test_route import assign_test_roles
from app.routes.ticketon.ticketon_route import assign_ticketon_roles
from app.routes.ticketon_order_status.ticketon_order_status_route import assign_ticketon_order_status_roles
from app.routes.ticketon_order.ticketon_order_route import assign_ticketon_order_roles
from app.routes.user.user_route import assign_user_roles
from app.routes.user_cart.user_cart_route import assign_user_cart_roles
from app.routes.user_code_verification.user_code_verification_route import assign_user_code_verification_roles
from app.routes.notification.notification_route import assign_notification_roles
from app.routes.read_notification.read_notification_route import assign_read_notification_roles
from app.routes.topic_notification.topic_notification_route import assign_topic_notification_roles
from app.routes.firebase_notification.firebase_notification_route import assign_firebase_notification_roles


def assign_roles_to_all_routes(app) -> None:
    # Academy related routes
    assign_academy_roles(app)
    assign_academy_gallery_roles(app)
    assign_academy_group_roles(app)
    assign_academy_group_schedule_roles(app)
    assign_academy_group_student_roles(app)
    assign_academy_material_roles(app)
    
    # Cart related routes
    assign_cart_roles(app)
    assign_cart_item_roles(app)
    
    # Category related routes
    assign_category_modification_roles(app)
    
    # Location related routes
    assign_city_roles(app)
    assign_country_roles(app)
    
    # Field related routes
    assign_field_roles(app)
    assign_field_gallery_roles(app)
    assign_field_party_roles(app)
    assign_field_party_schedule_roles(app)
    assign_field_party_schedule_settings_roles(app)
    
    # Modification related routes
    assign_modification_type_roles(app)
    assign_modification_value_roles(app)
    
    # Payment related routes
    assign_payment_transaction_status_roles(app)
    assign_payment_transaction_roles(app)
    
    # Product related routes
    assign_product_roles(app)
    assign_product_category_roles(app)
    assign_product_gallery_roles(app)
    assign_product_variant_roles(app)
    assign_product_variant_modification_roles(app)
    assign_product_order_roles(app)
    assign_product_order_admin_roles(app)
    assign_product_order_item_admin_roles(app)
    assign_product_order_status_roles(app)
    assign_product_order_item_status_roles(app)
    
    # Request related routes
    assign_request_material_roles(app)
    assign_request_to_academy_group_roles(app)
    
    # Sport and student routes
    assign_sport_roles(app)
    assign_student_roles(app)
    
    # System routes (User, Role, Permission)
    assign_role_roles(app)
    assign_permission_roles(app)
    assign_user_roles(app)
    assign_user_cart_roles(app)
    assign_user_code_verification_roles(app)

    #Test
    assign_test_roles(app)

    # Auth
    assign_auth_roles(app)
    
    # External API integrations
    assign_ticketon_roles(app)
    assign_ticketon_order_status_roles(app)
    assign_ticketon_order_roles(app)

    # Booking Field Party routes
    assign_booking_field_party_status_roles(app)
    assign_booking_field_party_request_roles(app)
    assign_booking_field_party_and_payment_transaction_roles(app)

    # Notification routes
    assign_notification_roles(app)
    assign_read_notification_roles(app)
    assign_topic_notification_roles(app)
    assign_firebase_notification_roles(app)
    #Sota
    assign_sota_roles(app)
