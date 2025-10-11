-- =====================================================
-- SQL скрипт для исправления всех Foreign Keys
-- Изменение SET NULL на CASCADE для non-nullable полей
-- =====================================================

-- ВАЖНО: Этот скрипт необходим, потому что Alembic может
-- создавать FK с SET NULL даже если в модели указан CASCADE

-- 1. Academies
ALTER TABLE academies DROP CONSTRAINT IF EXISTS academies_city_id_fkey;
ALTER TABLE academies ADD CONSTRAINT academies_city_id_fkey
    FOREIGN KEY (city_id) REFERENCES cities(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE academies DROP CONSTRAINT IF EXISTS academies_image_id_fkey;
ALTER TABLE academies ADD CONSTRAINT academies_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 2. Academy Galleries
ALTER TABLE academy_galleries DROP CONSTRAINT IF EXISTS academy_galleries_file_id_fkey;
ALTER TABLE academy_galleries ADD CONSTRAINT academy_galleries_file_id_fkey
    FOREIGN KEY (file_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE academy_galleries DROP CONSTRAINT IF EXISTS academy_galleries_group_id_fkey;
ALTER TABLE academy_galleries ADD CONSTRAINT academy_galleries_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES academy_groups(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 3. Academy Group Students
ALTER TABLE academy_group_students DROP CONSTRAINT IF EXISTS academy_group_students_request_id_fkey;
ALTER TABLE academy_group_students ADD CONSTRAINT academy_group_students_request_id_fkey
    FOREIGN KEY (request_id) REFERENCES request_to_academy_groups(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 4. Academy Groups
ALTER TABLE academy_groups DROP CONSTRAINT IF EXISTS academy_groups_image_id_fkey;
ALTER TABLE academy_groups ADD CONSTRAINT academy_groups_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 5. Academy Materials
ALTER TABLE academy_materials DROP CONSTRAINT IF EXISTS academy_materials_file_id_fkey;
ALTER TABLE academy_materials ADD CONSTRAINT academy_materials_file_id_fkey
    FOREIGN KEY (file_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE academy_materials DROP CONSTRAINT IF EXISTS academy_materials_group_id_fkey;
ALTER TABLE academy_materials ADD CONSTRAINT academy_materials_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES academy_groups(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 6. Booking Field Party Requests
ALTER TABLE booking_field_party_requests DROP CONSTRAINT IF EXISTS booking_field_party_requests_payment_transaction_id_fkey;
ALTER TABLE booking_field_party_requests ADD CONSTRAINT booking_field_party_requests_payment_transaction_id_fkey
    FOREIGN KEY (payment_transaction_id) REFERENCES payment_transactions(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE booking_field_party_requests DROP CONSTRAINT IF EXISTS booking_field_party_requests_status_id_fkey;
ALTER TABLE booking_field_party_requests ADD CONSTRAINT booking_field_party_requests_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES booking_field_party_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- 7. Cart Items
ALTER TABLE cart_items DROP CONSTRAINT IF EXISTS cart_items_variant_id_fkey;
ALTER TABLE cart_items ADD CONSTRAINT cart_items_variant_id_fkey
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 8. Category Modifications
ALTER TABLE category_modifications DROP CONSTRAINT IF EXISTS category_modifications_modification_type_id_fkey;
ALTER TABLE category_modifications ADD CONSTRAINT category_modifications_modification_type_id_fkey
    FOREIGN KEY (modification_type_id) REFERENCES modification_types(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 9. Field Galleries
ALTER TABLE field_galleries DROP CONSTRAINT IF EXISTS field_galleries_file_id_fkey;
ALTER TABLE field_galleries ADD CONSTRAINT field_galleries_file_id_fkey
    FOREIGN KEY (file_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE field_galleries DROP CONSTRAINT IF EXISTS field_galleries_party_id_fkey;
ALTER TABLE field_galleries ADD CONSTRAINT field_galleries_party_id_fkey
    FOREIGN KEY (party_id) REFERENCES field_parties(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 10. Field Parties
ALTER TABLE field_parties DROP CONSTRAINT IF EXISTS field_parties_image_id_fkey;
ALTER TABLE field_parties ADD CONSTRAINT field_parties_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 11. Fields
ALTER TABLE fields DROP CONSTRAINT IF EXISTS fields_city_id_fkey;
ALTER TABLE fields ADD CONSTRAINT fields_city_id_fkey
    FOREIGN KEY (city_id) REFERENCES cities(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE fields DROP CONSTRAINT IF EXISTS fields_image_id_fkey;
ALTER TABLE fields ADD CONSTRAINT fields_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 12. Payment Transactions
ALTER TABLE payment_transactions DROP CONSTRAINT IF EXISTS payment_transactions_status_id_fkey;
ALTER TABLE payment_transactions ADD CONSTRAINT payment_transactions_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES payment_transaction_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE payment_transactions DROP CONSTRAINT IF EXISTS payment_transactions_user_id_fkey;
ALTER TABLE payment_transactions ADD CONSTRAINT payment_transactions_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 13. Product Categories
ALTER TABLE product_categories DROP CONSTRAINT IF EXISTS product_categories_image_id_fkey;
ALTER TABLE product_categories ADD CONSTRAINT product_categories_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 14. Product Galleries
ALTER TABLE product_galleries DROP CONSTRAINT IF EXISTS product_galleries_file_id_fkey;
ALTER TABLE product_galleries ADD CONSTRAINT product_galleries_file_id_fkey
    FOREIGN KEY (file_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE product_galleries DROP CONSTRAINT IF EXISTS product_galleries_variant_id_fkey;
ALTER TABLE product_galleries ADD CONSTRAINT product_galleries_variant_id_fkey
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 15. Product Order Item Histories
ALTER TABLE product_order_item_histories DROP CONSTRAINT IF EXISTS product_order_item_histories_responsible_user_id_fkey;
ALTER TABLE product_order_item_histories ADD CONSTRAINT product_order_item_histories_responsible_user_id_fkey
    FOREIGN KEY (responsible_user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_order_item_histories DROP CONSTRAINT IF EXISTS product_order_item_histories_status_id_fkey;
ALTER TABLE product_order_item_histories ADD CONSTRAINT product_order_item_histories_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES product_order_item_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- 16. Product Order Item Verification Codes
ALTER TABLE product_order_item_verification_codes DROP CONSTRAINT IF EXISTS product_order_item_verification_codes_responsible_user_id_fkey;
ALTER TABLE product_order_item_verification_codes ADD CONSTRAINT product_order_item_verification_codes_responsible_user_id_fkey
    FOREIGN KEY (responsible_user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 17. Product Order Items
ALTER TABLE product_order_items DROP CONSTRAINT IF EXISTS product_order_items_canceled_by_id_fkey;
ALTER TABLE product_order_items ADD CONSTRAINT product_order_items_canceled_by_id_fkey
    FOREIGN KEY (canceled_by_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_order_items DROP CONSTRAINT IF EXISTS product_order_items_status_id_fkey;
ALTER TABLE product_order_items ADD CONSTRAINT product_order_items_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES product_order_item_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE product_order_items DROP CONSTRAINT IF EXISTS product_order_items_to_city_id_fkey;
ALTER TABLE product_order_items ADD CONSTRAINT product_order_items_to_city_id_fkey
    FOREIGN KEY (to_city_id) REFERENCES cities(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_order_items DROP CONSTRAINT IF EXISTS product_order_items_variant_id_fkey;
ALTER TABLE product_order_items ADD CONSTRAINT product_order_items_variant_id_fkey
    FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- 18. Product Orders
ALTER TABLE product_orders DROP CONSTRAINT IF EXISTS product_orders_canceled_by_id_fkey;
ALTER TABLE product_orders ADD CONSTRAINT product_orders_canceled_by_id_fkey
    FOREIGN KEY (canceled_by_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_orders DROP CONSTRAINT IF EXISTS product_orders_payment_transaction_id_fkey;
ALTER TABLE product_orders ADD CONSTRAINT product_orders_payment_transaction_id_fkey
    FOREIGN KEY (payment_transaction_id) REFERENCES payment_transactions(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_orders DROP CONSTRAINT IF EXISTS product_orders_status_id_fkey;
ALTER TABLE product_orders ADD CONSTRAINT product_orders_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES product_order_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- 19. Product Variants
ALTER TABLE product_variants DROP CONSTRAINT IF EXISTS product_variants_city_id_fkey;
ALTER TABLE product_variants ADD CONSTRAINT product_variants_city_id_fkey
    FOREIGN KEY (city_id) REFERENCES cities(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE product_variants DROP CONSTRAINT IF EXISTS product_variants_image_id_fkey;
ALTER TABLE product_variants ADD CONSTRAINT product_variants_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 20. Products
ALTER TABLE products DROP CONSTRAINT IF EXISTS products_category_id_fkey;
ALTER TABLE products ADD CONSTRAINT products_category_id_fkey
    FOREIGN KEY (category_id) REFERENCES product_categories(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE products DROP CONSTRAINT IF EXISTS products_city_id_fkey;
ALTER TABLE products ADD CONSTRAINT products_city_id_fkey
    FOREIGN KEY (city_id) REFERENCES cities(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE products DROP CONSTRAINT IF EXISTS products_image_id_fkey;
ALTER TABLE products ADD CONSTRAINT products_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 21. Request Materials
ALTER TABLE request_materials DROP CONSTRAINT IF EXISTS request_materials_file_id_fkey;
ALTER TABLE request_materials ADD CONSTRAINT request_materials_file_id_fkey
    FOREIGN KEY (file_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- 22. Request To Academy Groups
ALTER TABLE request_to_academy_groups DROP CONSTRAINT IF EXISTS request_to_academy_groups_checked_by_fkey;
ALTER TABLE request_to_academy_groups ADD CONSTRAINT request_to_academy_groups_checked_by_fkey
    FOREIGN KEY (checked_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 23. Students
ALTER TABLE students DROP CONSTRAINT IF EXISTS students_created_by_fkey;
ALTER TABLE students ADD CONSTRAINT students_created_by_fkey
    FOREIGN KEY (created_by) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE students DROP CONSTRAINT IF EXISTS students_image_id_fkey;
ALTER TABLE students ADD CONSTRAINT students_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 24. Ticketon Orders
ALTER TABLE ticketon_orders DROP CONSTRAINT IF EXISTS ticketon_orders_payment_transaction_id_fkey;
ALTER TABLE ticketon_orders ADD CONSTRAINT ticketon_orders_payment_transaction_id_fkey
    FOREIGN KEY (payment_transaction_id) REFERENCES payment_transactions(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE ticketon_orders DROP CONSTRAINT IF EXISTS ticketon_orders_status_id_fkey;
ALTER TABLE ticketon_orders ADD CONSTRAINT ticketon_orders_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES ticketon_order_statuses(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ticketon_orders DROP CONSTRAINT IF EXISTS ticketon_orders_user_id_fkey;
ALTER TABLE ticketon_orders ADD CONSTRAINT ticketon_orders_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 25. Topic Notifications
ALTER TABLE topic_notifications DROP CONSTRAINT IF EXISTS topic_notifications_image_id_fkey;
ALTER TABLE topic_notifications ADD CONSTRAINT topic_notifications_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- 26. Users
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_image_id_fkey;
ALTER TABLE users ADD CONSTRAINT users_image_id_fkey
    FOREIGN KEY (image_id) REFERENCES files(id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_id_fkey;
ALTER TABLE users ADD CONSTRAINT users_role_id_fkey
    FOREIGN KEY (role_id) REFERENCES roles(id) ON UPDATE CASCADE ON DELETE RESTRICT;

-- ПРИМЕЧАНИЯ:
-- CASCADE - используется для зависимых данных (galleries, materials, etc.)
-- SET NULL - используется для nullable полей (image_id, optional references)
-- RESTRICT - используется для критичных справочников (statuses, roles)
