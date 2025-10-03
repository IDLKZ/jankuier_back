from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import CartItemEntity, ProductEntity, ProductVariantEntity


class CartItemRepository(BaseRepository[CartItemEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(CartItemEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.cart),
            selectinload(self.model.product).selectinload(ProductEntity.image),
            selectinload(self.model.product).selectinload(ProductEntity.city),
            selectinload(self.model.product).selectinload(ProductEntity.category),
            selectinload(self.model.variant).selectinload(ProductVariantEntity.image),
            selectinload(self.model.variant).selectinload(ProductVariantEntity.product),
            selectinload(self.model.variant).selectinload(ProductVariantEntity.city),
        ]
