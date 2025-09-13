from typing import TYPE_CHECKING, Any
from pydantic import BaseModel
from app.adapters.dto.base_pagination_dto import BasePageModel
from app.shared.dto_constants import DTOConstant

if TYPE_CHECKING:
    from app.adapters.dto.user.user_dto import UserRDTO
    from app.adapters.dto.cart_item.cart_item_dto import CartItemRDTO


class CartDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class CartCDTO(BaseModel):
    user_id: DTOConstant.StandardUnsignedIntegerField(description="ID пользователя")
    total_price: DTOConstant.StandardZeroDecimalField(
        description="Общая стоимость корзины"
    )
    cart_items: DTOConstant.StandardNullableJSONField(
        description="Snapshot товаров в корзине в формате JSON"
    )

    class Config:
        from_attributes = True


class CartRDTO(CartDTO):
    user_id: DTOConstant.StandardUnsignedIntegerField(description="ID пользователя")
    total_price: DTOConstant.StandardZeroDecimalField(
        description="Общая стоимость корзины"
    )
    cart_items: DTOConstant.StandardNullableJSONField(
        description="Snapshot товаров в корзине в формате JSON"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt
    deleted_at: DTOConstant.StandardDeletedAt

    class Config:
        from_attributes = True


class CartWithRelationsRDTO(CartRDTO):
    user: "UserRDTO | None" = None
    cart_items_list: "list[CartItemRDTO] | None" = None

    class Config:
        from_attributes = True




class CartUpdateDTO(BaseModel):
    """DTO для обновления корзины"""

    total_price: (
        DTOConstant.StandardZeroDecimalField(description="Общая стоимость корзины")
        | None
    ) = None
    cart_items: (
        DTOConstant.StandardNullableJSONField(
            description="Snapshot товаров в корзине в формате JSON"
        )
        | None
    ) = None

    class Config:
        from_attributes = True


class CartCalculateTotalDTO(BaseModel):
    """DTO для пересчета общей стоимости корзины"""

    cart_id: DTOConstant.StandardUnsignedIntegerField(description="ID корзины")

    class Config:
        from_attributes = True


class PaginationCartRDTO(BasePageModel):
    items: list[CartRDTO]


class PaginationCartWithRelationsRDTO(BasePageModel):
    items: list[CartWithRelationsRDTO]


# Import the model rebuilder for backward compatibility
from app.adapters.dto.model_rebuilder import ensure_models_rebuilt

# Keep the old function name for backward compatibility
rebuild_cart_models = ensure_models_rebuilt
