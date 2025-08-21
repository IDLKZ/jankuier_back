from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.user.user_filter import UserFilter
from app.adapters.repository.user.user_repository import UserRepository
from app.use_case.base_case import BaseUseCase


class AllUserCase(BaseUseCase[list[UserWithRelationsRDTO]]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)

    async def execute(self, filter: UserFilter) -> list[UserWithRelationsRDTO]:
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [UserWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        pass
