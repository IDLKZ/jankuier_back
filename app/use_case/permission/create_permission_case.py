from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.permission.permission_dto import PermissionRDTO, PermissionCDTO
from app.adapters.repository.permission.permission_repository import (
    PermissionRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreatePermissionCase(BaseUseCase[PermissionRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = PermissionRepository(db)
        # Глобальные переменные
        self.dto: PermissionCDTO | None = None

    async def execute(self, dto: PermissionCDTO) -> PermissionRDTO:
        self.dto = dto
        await self.validate()
        model = await self.repository.create(self.repository.model(**self.dto.dict()))
        model = await self.repository.get(
            model.id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        return PermissionRDTO.from_orm(model)

    async def validate(
        self,
    ) -> None:
        if self.dto.value == None:
            self.dto.value = DbValueConstants.get_value(self.dto.title_ru)

        existed = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == self.dto.value.lower()],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{self.dto.value}"
            )

    async def transform(self):
        pass
