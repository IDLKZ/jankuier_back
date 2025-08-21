from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationPermissionRDTO
from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.adapters.filters.permission.permission_pagination_filter import (
    PermissionPaginationFilter,
)
from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)

from app.use_case.base_case import BaseUseCase


class PaginatePermissionCase(BaseUseCase[PaginationPermissionRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)

    async def execute(
        self, filter: PermissionPaginationFilter
    ) -> PaginationPermissionRDTO:
        models = await self.repository.paginate(
            dto=PermissionRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        pass
