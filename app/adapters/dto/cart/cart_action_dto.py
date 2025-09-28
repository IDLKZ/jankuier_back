from pydantic import BaseModel, Field

from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.dto.cart_item.cart_item_dto import CartItemWithRelationsRDTO


class AddToCartDTO(BaseModel):
    """DTO для добавления товара в корзину"""
    product_id: int = Field(..., gt=0, description="ID товара")
    qty: int = Field(default=1, gt=0, description="Количество товара")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")


class UpdateOrRemoveFromCartDTO(BaseModel):
    """DTO для удаления товара из корзины"""
    product_id: int = Field(..., gt=0, description="ID товара")
    updated_qty: int | None = Field(default=None, ge=0, description="Количество для обновления (если не указано - удаляет полностью)")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")
    remove_completely: bool = Field(default=False, description="Флаг полного удаления товара")


class CartActionResponseDTO(BaseModel):
    """DTO для действий в корзине"""
    cart:CartWithRelationsRDTO|None = None
    cart_items:list[CartItemWithRelationsRDTO]|None = []
    total_price:float = Field(..., ge=0, description="Общая стоимость корзины")