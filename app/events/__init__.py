from app.entities import CartItemEntity, ProductOrderEntity, ProductOrderItemEntity
from app.events.entity_event.cart_item_event.cart_item_event import CartItemEventHandler
from app.events.entity_event.product_order_event.product_order_event import ProductOrderEventHandler
from app.events.entity_event.product_order_item_event.product_order_item_event import ProductOrderItemEventHandler


def register_events():
    CartItemEventHandler.register(CartItemEntity)
    ProductOrderEventHandler.register(ProductOrderEntity)
    ProductOrderItemEventHandler.register(ProductOrderItemEntity)