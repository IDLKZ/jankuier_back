from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialWithRelationsRDTO,
)
from app.adapters.repository.request_material.request_material_repository import (
    RequestMaterialRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.use_case.base_case import BaseUseCase


class GetRequestMaterialByIdCase(BaseUseCase[RequestMaterialWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)

    async def execute(self, id: int) -> RequestMaterialWithRelationsRDTO:
        await self.validate(id)

        model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not model:
            raise AppExceptionResponse.not_found(message="RequestMaterial не найден")

        return RequestMaterialWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID должен быть положительным числом"
            )
