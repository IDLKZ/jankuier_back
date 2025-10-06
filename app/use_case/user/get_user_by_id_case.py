from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import UserEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetUserByIdCase(BaseUseCase[UserWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.model: UserEntity | None = None

    async def execute(self, id: int) -> UserWithRelationsRDTO:
        await self.validate(id=id)
        return UserWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("user_not_found"))
