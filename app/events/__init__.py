from app.entities import CartItemEntity
from app.events.entity_event.cart_item_event.cart_item_event import CartItemEventHandler


def register_events():
    CartItemEventHandler.register(CartItemEntity)