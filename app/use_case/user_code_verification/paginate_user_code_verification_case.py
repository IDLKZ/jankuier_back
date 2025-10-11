from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationUserCodeVerificationRDTO, \
    PaginationUserCodeVerificationWithRelationsRDTO
from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationWithRelationsRDTO,
)
from app.adapters.filters.user_code_verification.user_code_verification_filter import (
    UserCodeVerificationPaginationFilter,
)
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateUserCodeVerificationCase(BaseUseCase[PaginationUserCodeVerificationWithRelationsRDTO]):
    """Use case для пагинации кодов верификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)

    async def execute(
        self, filter_params: UserCodeVerificationPaginationFilter
    ) -> PaginationUserCodeVerificationWithRelationsRDTO:
        """Получить пагинированный список кодов верификации"""
        await self.validate(filter_params=filter_params)

        # Получение пагинированных данных
        pagination = await self.repository.paginate(
            dto=UserCodeVerificationWithRelationsRDTO,
            page=filter_params.page,
            per_page=filter_params.per_page,
            filters=filter_params.apply(),
            options=self.repository.default_relationships(),
            order_by=filter_params.order_by,
            order_direction=filter_params.order_direction,
            include_deleted_filter=filter_params.is_show_deleted,
        )

        return PaginationUserCodeVerificationRDTO.model_validate(pagination)

    async def validate(
        self, filter_params: UserCodeVerificationPaginationFilter
    ) -> None:
        """Валидация не требуется"""
        pass

    async def transform(self, **kwargs) -> None:
        """Трансформация не требуется"""
        pass
