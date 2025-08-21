from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.permission.permission_dto import PermissionRDTO, PermissionCDTO
from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PermissionEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class UpdatePermissionCase(BaseUseCase[PermissionRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)
        # Глобальные переменные
        self.dto: PermissionCDTO | None = None
        self.id: int | None = None
        self.model: PermissionEntity | None = None

    async def execute(self, id: int, dto: PermissionCDTO) -> PermissionRDTO:
        self.dto = dto
        self.id = id
        await self.validate()
        model = await self.repository.update(obj=self.model, dto=self.dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return PermissionRDTO.from_orm(model)

    async def validate(
        self,
    ) -> None:
        if self.dto.value == None:
            self.dto.value = DbValueConstants.get_value(self.dto.title_ru)
        self.model = await self.repository.get(self.id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("permission_not_found")
            )
        existed = await self.repository.get_first_with_filters(
            filters=[
                func.lower(self.repository.model.value) == self.dto.value.lower(),
                self.repository.model.id != self.id,
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{self.dto.value}"
            )

    async def transform(self):
        pass
