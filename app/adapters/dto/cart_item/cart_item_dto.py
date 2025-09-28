from pydantic import BaseModel
from app.adapters.dto.cart.cart_dto import CartRDTO
from app.adapters.dto.base_pagination_dto import BasePageModel
from app.adapters.dto.product.product_dto import ProductRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantRDTO
from app.shared.dto_constants import DTOConstant


class CartItemDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class CartItemCDTO(BaseModel):
    cart_id: DTOConstant.StandardUnsignedIntegerField(description="ID корзины")
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID варианта товара (опционально)"
    )
    qty: DTOConstant.StandardIntegerField(description="Количество товара")
    sku: DTOConstant.StandardNullableVarcharField(description="Артикул товара")
    product_price: DTOConstant.StandardPriceField(description="Базовая цена товара")
    delta_price: DTOConstant.StandardZeroDecimalField(
        description="Дельта цены (надбавка/скидка)"
    )
    class Config:
        from_attributes = True


class CartItemRDTO(CartItemDTO):
    cart_id: DTOConstant.StandardUnsignedIntegerField(description="ID корзины")
    product_id: DTOConstant.StandardUnsignedIntegerField(description="ID товара")
    variant_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID варианта товара (опционально)"
    )
    qty: DTOConstant.StandardIntegerField(description="Количество товара")
    sku: DTOConstant.StandardNullableVarcharField(description="Артикул товара")
    product_price: DTOConstant.StandardPriceField(description="Базовая цена товара")
    delta_price: DTOConstant.StandardZeroDecimalField(
        description="Дельта цены (надбавка/скидка)"
    )
    unit_price: DTOConstant.StandardDecimalField(
        description="Цена за единицу (базовая цена + дельта)"
    )
    total_price: DTOConstant.StandardDecimalField(
        description="Общая стоимость (цена за единицу * количество)"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class CartItemWithRelationsRDTO(CartItemRDTO):
    product: ProductRDTO | None = None
    variant: ProductVariantRDTO | None = None

    class Config:
        from_attributes = True


class CartItemUpdateDTO(BaseModel):
    """DTO для обновления элемента корзины"""

    qty: DTOConstant.StandardIntegerField(description="Количество товара") | None = None
    delta_price: (
        DTOConstant.StandardZeroDecimalField(
            description="Дельта цены (надбавка/скидка)"
        )
        | None
    ) = None

    class Config:
        from_attributes = True


class CartItemBulkCDTO(BaseModel):
    """DTO для массового добавления товаров в корзину"""

    cart_id: DTOConstant.StandardUnsignedIntegerField(description="ID корзины")
    items: list[dict] = (
        []
    )  # [{"product_id": 1, "variant_id": None, "qty": 2, "delta_price": 0}]

    class Config:
        from_attributes = True


class CartItemBulkUpdateQtyDTO(BaseModel):
    """DTO для массового обновления количества товаров в корзине"""

    cart_item_updates: list[dict] = (
        []
    )  # [{"cart_item_id": 1, "qty": 3}, {"cart_item_id": 2, "qty": 1}]

    class Config:
        from_attributes = True


class PaginationCartItemRDTO(BasePageModel):
    items: list[CartItemRDTO]


class PaginationCartItemWithRelationsRDTO(BasePageModel):
    items: list[CartItemWithRelationsRDTO]
