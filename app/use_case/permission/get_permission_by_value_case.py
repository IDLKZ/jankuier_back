from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.permission.permission_dto import PermissionRDTO
from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PermissionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetPermissionByValueCase(BaseUseCase[PermissionRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)
        self.model: PermissionEntity | None = None

    async def execute(self, value: str) -> PermissionRDTO:
        await self.validate(value=value)
        return PermissionRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
