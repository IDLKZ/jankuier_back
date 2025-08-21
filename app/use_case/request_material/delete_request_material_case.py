from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.request_material.request_material_repository import (
    RequestMaterialRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestMaterialEntity
from app.infrastructure.service.file_service import FileService
from app.shared.dto_constants import DTOConstant
from app.use_case.base_case import BaseUseCase


class DeleteRequestMaterialCase(BaseUseCase[DTOConstant.StandardResponseDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RequestMaterialRepository(db)
        self.file_service = FileService(db)
        self.model: RequestMaterialEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False
    ) -> DTOConstant.StandardResponseDTO:
        await self.validate(id)

        if self.model.file_id:
            await self.file_service.delete_file(file_id=self.model.file_id)

        await self.repository.delete(id=id, force_delete=force_delete)

        return DTOConstant.StandardResponseDTO(message="Материал заявки успешно удален")

    async def validate(self, id: int) -> None:
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID должен быть положительным числом"
            )

        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message="Материал заявки не найден")
