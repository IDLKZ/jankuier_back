from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import ProductVariantEntity


class ProductVariantRepository(BaseRepository[ProductVariantEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProductVariantEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.product),
            selectinload(self.model.image),
            selectinload(self.model.city),
        ]
