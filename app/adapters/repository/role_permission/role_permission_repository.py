from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import RolePermissionEntity


class RolePermissionRepository(BaseRepository[RolePermissionEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(RolePermissionEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.role),
            selectinload(self.model.permission),
        ]
