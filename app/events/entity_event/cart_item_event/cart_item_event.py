from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload

from app.entities import CartEntity, CartItemEntity, ProductEntity, ProductVariantEntity
from app.events.entity_event.entity_event_handler import EntityEventHandler


class CartItemEventHandler(EntityEventHandler):
    @staticmethod
    def after_insert(mapper, connection, target):
        CartItemEventHandler._update_cart_data(connection, target)

    @staticmethod
    def after_update(mapper, connection, target):
        CartItemEventHandler._update_cart_data(connection, target)

    @staticmethod
    def after_delete(mapper, connection, target):
        CartItemEventHandler._update_cart_data(connection, target)

    @staticmethod
    def _update_cart_data(connection, target):
        """Обновление суммы и cart_items в Cart после изменений CartItem"""
        # Обновляем total_price
        CartItemEventHandler._update_cart_total(connection, target)

        # Обновляем cart_items snapshot
        CartItemEventHandler._update_cart_items_snapshot(connection, target)

    @staticmethod
    def _update_cart_total(connection, target):
        """Обновление суммы в Cart после изменений CartItem"""
        connection.execute(
            update(CartEntity)
            .where(CartEntity.id == target.cart_id)
            .values(
                total_price=(
                    select(func.coalesce(func.sum(CartItemEntity.total_price), 0))
                    .where(
                        (CartItemEntity.cart_id == target.cart_id) &
                        (CartItemEntity.deleted_at.is_(None))
                    )
                    .scalar_subquery()
                )
            )
        )

    @staticmethod
    def _update_cart_items_snapshot(connection, target):
        """Обновление cart_items snapshot в Cart с полными CartItemEntity данными включая relationships"""
        # Получаем все активные cart_items для корзины с их связанными данными
        cart_items_query = (
            select(
                # CartItem fields
                CartItemEntity.id,
                CartItemEntity.cart_id,
                CartItemEntity.product_id,
                CartItemEntity.variant_id,
                CartItemEntity.qty,
                CartItemEntity.sku,
                CartItemEntity.product_price,
                CartItemEntity.delta_price,
                CartItemEntity.unit_price,
                CartItemEntity.total_price,
                CartItemEntity.created_at,
                CartItemEntity.updated_at,
                CartItemEntity.deleted_at,
                # Product fields
                ProductEntity.id.label('product_id_full'),
                ProductEntity.image_id.label('product_image_id'),
                ProductEntity.city_id.label('product_city_id'),
                ProductEntity.category_id.label('product_category_id'),
                ProductEntity.title_ru.label('product_title_ru'),
                ProductEntity.title_kk.label('product_title_kk'),
                ProductEntity.title_en.label('product_title_en'),
                ProductEntity.description_ru.label('product_description_ru'),
                ProductEntity.description_kk.label('product_description_kk'),
                ProductEntity.description_en.label('product_description_en'),
                ProductEntity.value.label('product_value'),
                ProductEntity.sku.label('product_sku'),
                ProductEntity.base_price.label('product_base_price'),
                ProductEntity.old_price.label('product_old_price'),
                ProductEntity.stock.label('product_stock'),
                ProductEntity.gender.label('product_gender'),
                ProductEntity.is_for_children.label('product_is_for_children'),
                ProductEntity.is_recommended.label('product_is_recommended'),
                ProductEntity.is_active.label('product_is_active'),
                ProductEntity.created_at.label('product_created_at'),
                ProductEntity.updated_at.label('product_updated_at'),
                ProductEntity.deleted_at.label('product_deleted_at'),
                # ProductVariant fields
                ProductVariantEntity.id.label('variant_id_full'),
                ProductVariantEntity.product_id.label('variant_product_id'),
                ProductVariantEntity.image_id.label('variant_image_id'),
                ProductVariantEntity.city_id.label('variant_city_id'),
                ProductVariantEntity.title_ru.label('variant_title_ru'),
                ProductVariantEntity.title_kk.label('variant_title_kk'),
                ProductVariantEntity.title_en.label('variant_title_en'),
                ProductVariantEntity.value.label('variant_value'),
                ProductVariantEntity.sku.label('variant_sku'),
                ProductVariantEntity.price_delta.label('variant_price_delta'),
                ProductVariantEntity.stock.label('variant_stock'),
                ProductVariantEntity.is_active.label('variant_is_active'),
                ProductVariantEntity.is_default.label('variant_is_default'),
                ProductVariantEntity.created_at.label('variant_created_at'),
                ProductVariantEntity.updated_at.label('variant_updated_at'),
                ProductVariantEntity.deleted_at.label('variant_deleted_at'),
            )
            .select_from(
                CartItemEntity
            )
            .join(ProductEntity, CartItemEntity.product_id == ProductEntity.id)
            .outerjoin(ProductVariantEntity, CartItemEntity.variant_id == ProductVariantEntity.id)
            .where(
                (CartItemEntity.cart_id == target.cart_id) &
                (CartItemEntity.deleted_at.is_(None))
            )
        )

        cart_items_result = connection.execute(cart_items_query).fetchall()

        # Формируем структуру CartItemEntity с relationships для cart_items
        cart_items_data = []
        for row in cart_items_result:
            # CartItem данные
            cart_item = {
                "id": row.id,
                "cart_id": row.cart_id,
                "product_id": row.product_id,
                "variant_id": row.variant_id,
                "qty": row.qty,
                "sku": row.sku,
                "product_price": float(row.product_price) if row.product_price else 0.0,
                "delta_price": float(row.delta_price) if row.delta_price else 0.0,
                "unit_price": float(row.unit_price) if row.unit_price else 0.0,
                "total_price": float(row.total_price) if row.total_price else 0.0,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None,

                # Product relationship
                "product": {
                    "id": row.product_id_full,
                    "image_id": row.product_image_id,
                    "city_id": row.product_city_id,
                    "category_id": row.product_category_id,
                    "title_ru": row.product_title_ru,
                    "title_kk": row.product_title_kk,
                    "title_en": row.product_title_en,
                    "description_ru": row.product_description_ru,
                    "description_kk": row.product_description_kk,
                    "description_en": row.product_description_en,
                    "value": row.product_value,
                    "sku": row.product_sku,
                    "base_price": float(row.product_base_price) if row.product_base_price else 0.0,
                    "old_price": float(row.product_old_price) if row.product_old_price else None,
                    "stock": row.product_stock,
                    "gender": row.product_gender,
                    "is_for_children": row.product_is_for_children,
                    "is_recommended": row.product_is_recommended,
                    "is_active": row.product_is_active,
                    "created_at": row.product_created_at.isoformat() if row.product_created_at else None,
                    "updated_at": row.product_updated_at.isoformat() if row.product_updated_at else None,
                    "deleted_at": row.product_deleted_at.isoformat() if row.product_deleted_at else None,
                },

                # Variant relationship (если есть)
                "variant": {
                    "id": row.variant_id_full,
                    "product_id": row.variant_product_id,
                    "image_id": row.variant_image_id,
                    "city_id": row.variant_city_id,
                    "title_ru": row.variant_title_ru,
                    "title_kk": row.variant_title_kk,
                    "title_en": row.variant_title_en,
                    "value": row.variant_value,
                    "sku": row.variant_sku,
                    "price_delta": float(row.variant_price_delta) if row.variant_price_delta else 0.0,
                    "stock": row.variant_stock,
                    "is_active": row.variant_is_active,
                    "is_default": row.variant_is_default,
                    "created_at": row.variant_created_at.isoformat() if row.variant_created_at else None,
                    "updated_at": row.variant_updated_at.isoformat() if row.variant_updated_at else None,
                    "deleted_at": row.variant_deleted_at.isoformat() if row.variant_deleted_at else None,
                } if row.variant_id else None,
            }
            cart_items_data.append(cart_item)

        # Обновляем cart_items в Cart
        connection.execute(
            update(CartEntity)
            .where(CartEntity.id == target.cart_id)
            .values(cart_items=cart_items_data)
        )
