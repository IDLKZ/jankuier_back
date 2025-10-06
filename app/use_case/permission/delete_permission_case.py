from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PermissionEntity

from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeletePermissionByIdCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)
        self.model: PermissionEntity | None = None
        self.file_service = FileService(db)

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
