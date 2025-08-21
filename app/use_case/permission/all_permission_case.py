from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationPermissionRDTO
from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.adapters.filters.permission.permission_filter import PermissionFilter
from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)
from app.use_case.base_case import BaseUseCase


class AllPermissionCase(BaseUseCase[list[PermissionRDTO]]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)

    async def execute(self, filter: PermissionFilter) -> list[PermissionRDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [PermissionRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        pass
