from app.entities import CartItemEntity, ProductOrderEntity
from app.events.entity_event.cart_item_event.cart_item_event import CartItemEventHandler
from app.events.entity_event.product_order_event.product_order_event import ProductOrderEventHandler


def register_events():
    CartItemEventHandler.register(CartItemEntity)
    ProductOrderEventHandler.register(ProductOrderEntity)