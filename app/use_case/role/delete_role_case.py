from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RoleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteRoleByIdCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RoleRepository(db)
        self.model: RoleEntity | None = None

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        return await self.repository.delete(id=id)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
        if self.model.is_system:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("can_not_delete_system_role")
            )
