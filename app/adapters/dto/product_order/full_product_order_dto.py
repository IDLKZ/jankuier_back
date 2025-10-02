from typing import List

from pydantic import BaseModel

from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO


class FullProductOrderRDTO(BaseModel):
    product_order: ProductOrderWithRelationsRDTO|None = None
    product_order_items: List[ProductOrderItemWithRelationsRDTO]|None = []

    class Config:
        from_attributes = True