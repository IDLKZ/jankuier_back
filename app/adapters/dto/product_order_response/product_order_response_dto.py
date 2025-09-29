from typing import Any

from pydantic import BaseModel


class ProductOrderResponseDTO(BaseModel):
    product_order: Any | None = None
    product_order_items: list[Any] | None = None
    order: Any | None = None
    payment_transaction: Any | None = None
    is_success: bool = False
    message: str = "OK"

class ProductOrderWithPaymentTransactionResponseDTO(BaseModel):
    product_order: Any | None = None
    product_order_items:list[Any] | None = None
    payment_transaction: Any | None = None
    is_success: bool = False
    message: str = "OK"

