from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationWithRelationsRDTO,
)
from app.adapters.filters.user_code_verification.user_code_verification_filter import (
    UserCodeVerificationFilter,
)
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.use_case.base_case import BaseUseCase


class AllUserCodeVerificationCase(BaseUseCase[list[UserCodeVerificationWithRelationsRDTO]]):
    """Use case для получения всех кодов верификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)

    async def execute(
        self, filter_params: UserCodeVerificationFilter
    ) -> list[UserCodeVerificationWithRelationsRDTO]:
        """Получить все коды верификации"""
        await self.validate(filter_params=filter_params)

        # Получение всех данных
        verifications = await self.repository.get_with_filters(
            filters=filter_params.apply(),
            options=self.repository.default_relationships(),
            order_by=filter_params.order_by,
            order_direction=filter_params.order_direction,
            include_deleted_filter=filter_params.is_show_deleted,
        )

        return [
            UserCodeVerificationWithRelationsRDTO.model_validate(v)
            for v in verifications
        ]

    async def validate(self, filter_params: UserCodeVerificationFilter) -> None:
        """Валидация не требуется"""
        pass

    async def transform(self, **kwargs) -> None:
        """Трансформация не требуется"""
        pass
