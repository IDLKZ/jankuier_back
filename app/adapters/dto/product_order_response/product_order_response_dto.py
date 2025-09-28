from typing import List, Optional, Any

from pydantic import BaseModel



class ProductOrderResponseDTO(BaseModel):
    product_order:Any
    product_order_items: Any
    order:Any
    payment_transaction: Any
    is_success: bool = False
    message: str = "OK"