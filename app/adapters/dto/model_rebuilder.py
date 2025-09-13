"""
Module to handle Pydantic model rebuilding for forward references.
This module should be imported after all DTOs are defined to resolve circular dependencies.
"""

def rebuild_all_models():
    """Rebuild all models that have forward references"""
    try:
        # Import all the DTO modules that need rebuilding
        from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO, PaginationCartWithRelationsRDTO
        from app.adapters.dto.user.user_dto import UserRDTO
        from app.adapters.dto.cart_item.cart_item_dto import CartItemRDTO
        
        # Rebuild models with forward references
        CartWithRelationsRDTO.model_rebuild()
        PaginationCartWithRelationsRDTO.model_rebuild()
        
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