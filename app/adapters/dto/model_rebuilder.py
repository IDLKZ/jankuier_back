"""
Module to handle Pydantic model rebuilding for forward references.
This module should be imported after all DTOs are defined to resolve circular dependencies.
"""

def rebuild_all_models():
    """Rebuild all models that have forward references"""
    try:
        # Import all the DTO modules that need rebuilding
        from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO, PaginationCartWithRelationsRDTO
        from app.adapters.dto.cart.cart_action_dto import CartActionResponseDTO
        from app.adapters.dto.user.user_dto import UserRDTO
        from app.adapters.dto.cart_item.cart_item_dto import CartItemRDTO, CartItemWithRelationsRDTO
        from app.adapters.dto.product_order.product_order_dto import ProductOrderRDTO
        from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO, ProductOrderItemRDTO

        # Import all referenced DTOs for ProductOrderItemWithRelationsRDTO
        from app.adapters.dto.product_order_item_status.product_order_item_status_dto import ProductOrderItemStatusRDTO
        from app.adapters.dto.product.product_dto import ProductRDTO
        from app.adapters.dto.product_variant.product_variant_dto import ProductVariantRDTO
        from app.adapters.dto.city.city_dto import CityRDTO
        from app.adapters.dto.product_order_item_history.product_order_item_history_dto import ProductOrderItemHistoryRDTO, ProductOrderItemHistoryWithRelationsRDTO
        from app.adapters.dto.product_order_item_verification.product_order_item_verification_dto import ProductOrderItemVerificationCodeWithRelationsRDTO
        from app.adapters.dto.product_item_history.product_item_history_dto import ProductOrderItemHistoryWithRelationsRDTO as ProductItemHistoryWithRelationsRDTO
        from app.adapters.dto.product_order_and_payment_transaction.product_order_and_payment_transaction_dto import ProductOrderAndPaymentTransactionWithRelationsRDTO
        from app.adapters.dto.pagination_dto import PaginationProductOrderWithRelationsRDTO, PaginationProductOrderItemWithRelationsRDTO

        # Rebuild models with forward references
        CartWithRelationsRDTO.model_rebuild()
        CartItemWithRelationsRDTO.model_rebuild()
        CartActionResponseDTO.model_rebuild()
        PaginationCartWithRelationsRDTO.model_rebuild()
        ProductOrderItemWithRelationsRDTO.model_rebuild()
        ProductOrderItemHistoryWithRelationsRDTO.model_rebuild()
        ProductOrderItemVerificationCodeWithRelationsRDTO.model_rebuild()
        ProductItemHistoryWithRelationsRDTO.model_rebuild()
        ProductOrderAndPaymentTransactionWithRelationsRDTO.model_rebuild()
        PaginationProductOrderWithRelationsRDTO.model_rebuild()
        PaginationProductOrderItemWithRelationsRDTO.model_rebuild()

        return True
    except ImportError as e:
        print(f"Could not rebuild models: {e}")
        return False

# Global flag to track if models have been rebuilt
_models_rebuilt = False

def ensure_models_rebuilt():
    """Ensure models are rebuilt exactly once"""
    global _models_rebuilt
    if not _models_rebuilt:
        _models_rebuilt = rebuild_all_models()
    return _models_rebuilt