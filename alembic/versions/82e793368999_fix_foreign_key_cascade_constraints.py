"""fix_foreign_key_cascade_constraints

Revision ID: 82e793368999
Revises: cf0df4146ff5
Create Date: 2025-10-11 10:29:42.380118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82e793368999'
down_revision: Union[str, None] = 'cf0df4146ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Исправление всех foreign keys с неправильными CASCADE constraints.

    ПРОБЛЕМА: Alembic может создавать FK с SET NULL даже если в модели указан CASCADE.
    РЕШЕНИЕ: Явное пересоздание всех FK с правильными constraints.

    Типы constraints:
    - CASCADE: для зависимых записей (galleries, items, etc.)
    - SET NULL: для nullable полей (image_id, optional references)
    - RESTRICT: для критичных справочников (statuses, roles)
    """

    # ============= CASCADE - зависимые данные =============
    # Эти записи должны удаляться вместе с родительскими
    cascade_fks = [
        ('academy_galleries', 'academy_galleries_file_id_fkey', 'file_id', 'files', 'id'),
        ('academy_galleries', 'academy_galleries_group_id_fkey', 'group_id', 'academy_groups', 'id'),
        ('academy_group_students', 'academy_group_students_request_id_fkey', 'request_id', 'request_to_academy_groups', 'id'),
        ('academy_materials', 'academy_materials_file_id_fkey', 'file_id', 'files', 'id'),
        ('academy_materials', 'academy_materials_group_id_fkey', 'group_id', 'academy_groups', 'id'),
        ('cart_items', 'cart_items_variant_id_fkey', 'variant_id', 'product_variants', 'id'),
        ('category_modifications', 'category_modifications_modification_type_id_fkey', 'modification_type_id', 'modification_types', 'id'),
        ('field_galleries', 'field_galleries_file_id_fkey', 'file_id', 'files', 'id'),
        ('field_galleries', 'field_galleries_party_id_fkey', 'party_id', 'field_parties', 'id'),
        ('product_galleries', 'product_galleries_file_id_fkey', 'file_id', 'files', 'id'),
        ('product_galleries', 'product_galleries_variant_id_fkey', 'variant_id', 'product_variants', 'id'),
        ('request_materials', 'request_materials_file_id_fkey', 'file_id', 'files', 'id'),
    ]

    for table, constraint, column, ref_table, ref_column in cascade_fks:
        op.drop_constraint(constraint, table, type_='foreignkey')
        op.create_foreign_key(
            constraint, table, ref_table,
            [column], [ref_column],
            onupdate='CASCADE', ondelete='CASCADE'
        )

    # ============= RESTRICT - критичные справочники =============
    # Запрещаем удаление если есть зависимые записи
    restrict_fks = [
        ('booking_field_party_requests', 'booking_field_party_requests_status_id_fkey', 'status_id', 'booking_field_party_statuses', 'id'),
        ('payment_transactions', 'payment_transactions_status_id_fkey', 'status_id', 'payment_transaction_statuses', 'id'),
        ('product_order_item_histories', 'product_order_item_histories_status_id_fkey', 'status_id', 'product_order_item_statuses', 'id'),
        ('product_order_items', 'product_order_items_status_id_fkey', 'status_id', 'product_order_item_statuses', 'id'),
        ('product_order_items', 'product_order_items_variant_id_fkey', 'variant_id', 'product_variants', 'id'),
        ('product_orders', 'product_orders_status_id_fkey', 'status_id', 'product_order_statuses', 'id'),
        ('ticketon_orders', 'ticketon_orders_status_id_fkey', 'status_id', 'ticketon_order_statuses', 'id'),
        ('users', 'users_role_id_fkey', 'role_id', 'roles', 'id'),
    ]

    for table, constraint, column, ref_table, ref_column in restrict_fks:
        op.drop_constraint(constraint, table, type_='foreignkey')
        op.create_foreign_key(
            constraint, table, ref_table,
            [column], [ref_column],
            onupdate='CASCADE', ondelete='RESTRICT'
        )

    # ============= SET NULL - nullable опциональные поля =============
    # Устанавливаем NULL при удалении родительской записи
    set_null_fks = [
        ('academies', 'academies_city_id_fkey', 'city_id', 'cities', 'id'),
        ('academies', 'academies_image_id_fkey', 'image_id', 'files', 'id'),
        ('academy_groups', 'academy_groups_image_id_fkey', 'image_id', 'files', 'id'),
        ('booking_field_party_requests', 'booking_field_party_requests_payment_transaction_id_fkey', 'payment_transaction_id', 'payment_transactions', 'id'),
        ('field_parties', 'field_parties_image_id_fkey', 'image_id', 'files', 'id'),
        ('fields', 'fields_city_id_fkey', 'city_id', 'cities', 'id'),
        ('fields', 'fields_image_id_fkey', 'image_id', 'files', 'id'),
        ('payment_transactions', 'payment_transactions_user_id_fkey', 'user_id', 'users', 'id'),
        ('product_categories', 'product_categories_image_id_fkey', 'image_id', 'files', 'id'),
        ('product_order_item_histories', 'product_order_item_histories_responsible_user_id_fkey', 'responsible_user_id', 'users', 'id'),
        ('product_order_item_verification_codes', 'product_order_item_verification_codes_responsible_user_id_fkey', 'responsible_user_id', 'users', 'id'),
        ('product_order_items', 'product_order_items_canceled_by_id_fkey', 'canceled_by_id', 'users', 'id'),
        ('product_order_items', 'product_order_items_to_city_id_fkey', 'to_city_id', 'cities', 'id'),
        ('product_orders', 'product_orders_canceled_by_id_fkey', 'canceled_by_id', 'users', 'id'),
        ('product_orders', 'product_orders_payment_transaction_id_fkey', 'payment_transaction_id', 'payment_transactions', 'id'),
        ('product_variants', 'product_variants_city_id_fkey', 'city_id', 'cities', 'id'),
        ('product_variants', 'product_variants_image_id_fkey', 'image_id', 'files', 'id'),
        ('products', 'products_category_id_fkey', 'category_id', 'product_categories', 'id'),
        ('products', 'products_city_id_fkey', 'city_id', 'cities', 'id'),
        ('products', 'products_image_id_fkey', 'image_id', 'files', 'id'),
        ('request_to_academy_groups', 'request_to_academy_groups_checked_by_fkey', 'checked_by', 'users', 'id'),
        ('students', 'students_created_by_fkey', 'created_by', 'users', 'id'),
        ('students', 'students_image_id_fkey', 'image_id', 'files', 'id'),
        ('ticketon_orders', 'ticketon_orders_payment_transaction_id_fkey', 'payment_transaction_id', 'payment_transactions', 'id'),
        ('ticketon_orders', 'ticketon_orders_user_id_fkey', 'user_id', 'users', 'id'),
        ('topic_notifications', 'topic_notifications_image_id_fkey', 'image_id', 'files', 'id'),
        ('users', 'users_image_id_fkey', 'image_id', 'files', 'id'),
    ]

    for table, constraint, column, ref_table, ref_column in set_null_fks:
        op.drop_constraint(constraint, table, type_='foreignkey')
        op.create_foreign_key(
            constraint, table, ref_table,
            [column], [ref_column],
            onupdate='CASCADE', ondelete='SET NULL'
        )


def downgrade() -> None:
    """
    Откат миграции - возвращаем все FK в состояние SET NULL.
    ВНИМАНИЕ: Не рекомендуется использовать downgrade, так как это вернет проблему.
    """
    # Откат не реализован, так как возвращение к SET NULL вернет проблему
    pass
