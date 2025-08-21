from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialWithRelationsRDTO,
)
from app.adapters.filters.request_material.request_material_filter import (
    RequestMaterialFilter,
)
from app.adapters.repository.request_material.request_material_repository import (
    RequestMaterialRepository,
)
from app.use_case.base_case import BaseUseCase


class AllRequestMaterialCase(BaseUseCase[list[RequestMaterialWithRelationsRDTO]]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)

    async def execute(
        self, filter: RequestMaterialFilter
    ) -> list[RequestMaterialWithRelationsRDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [RequestMaterialWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        pass
