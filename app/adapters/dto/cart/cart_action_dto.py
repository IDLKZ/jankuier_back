from pydantic import BaseModel, Field


class AddToCartDTO(BaseModel):
    """DTO для добавления товара в корзину"""
    product_id: int = Field(..., gt=0, description="ID товара")
    qty: int = Field(default=1, gt=0, description="Количество товара")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")


class RemoveFromCartDTO(BaseModel):
    """DTO для удаления товара из корзины"""
    product_id: int = Field(..., gt=0, description="ID товара")
    qty_to_remove: int | None = Field(default=None, gt=0, description="Количество для удаления (если не указано - удаляет полностью)")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")
    remove_completely: bool = Field(default=False, description="Флаг полного удаления товара")