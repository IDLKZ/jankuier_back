from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleRDTO
from app.adapters.repository.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RoleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetRoleByValueCase(BaseUseCase[RoleRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RoleRepository(db)
        self.model: RoleEntity | None = None

    async def execute(self, value: str) -> RoleRDTO:
        await self.validate(value=value)
        return RoleRDTO.from_orm(self.model)

    async def validate(self, value: str) -> None:
        self.model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
