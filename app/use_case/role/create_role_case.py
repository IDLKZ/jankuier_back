from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.role.role_dto import RoleCDTO, RoleRDTO
from app.adapters.repository.role.role_repository import RoleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RoleEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateRoleCase(BaseUseCase[RoleRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = RoleRepository(db)
        self.model: RoleEntity | None = None

    async def execute(self, dto: RoleCDTO) -> RoleRDTO:
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return RoleRDTO.from_orm(model)

    async def validate(self, dto: RoleCDTO) -> None:
        if dto.value == None:
            dto.value = DbValueConstants.get_value(dto.title_ru)
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext("the_next_value_already_exists")}{dto.value}"
            )
        self.model = RoleEntity(**dto.dict())
