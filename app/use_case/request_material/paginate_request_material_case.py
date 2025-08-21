from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationRequestMaterialWithRelationsRDTO
from app.adapters.dto.request_material.request_material_dto import RequestMaterialWithRelationsRDTO
from app.adapters.filters.request_material.request_material_pagination_filter import RequestMaterialPaginationFilter
from app.adapters.repository.request_material.request_material_repository import RequestMaterialRepository
from app.use_case.base_case import BaseUseCase


class PaginateRequestMaterialCase(BaseUseCase[PaginationRequestMaterialWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)

    async def execute(self, filter: RequestMaterialPaginationFilter) -> PaginationRequestMaterialWithRelationsRDTO:
        pagination = await self.repository.paginate(
            dto=RequestMaterialWithRelationsRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            page=filter.page,
            per_page=filter.per_page,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return PaginationRequestMaterialWithRelationsRDTO(**pagination.dict())

    async def validate(self) -> None:
        pass