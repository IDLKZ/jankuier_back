from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationUserWithRelationsRDTO
from app.adapters.filters.user.user_pagination_filter import UserPaginationFilter
from app.adapters.repository.user.user_repository import UserRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO


class PaginateUserCase(BaseUseCase[PaginationUserWithRelationsRDTO]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)

    async def execute(
        self, filter: UserPaginationFilter
    ) -> PaginationUserWithRelationsRDTO:
        models = await self.repository.paginate(
            dto=UserWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        pass
