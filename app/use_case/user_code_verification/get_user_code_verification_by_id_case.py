from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationWithRelationsRDTO,
)
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetUserCodeVerificationByIdCase(
    BaseUseCase[UserCodeVerificationWithRelationsRDTO]
):
    """Use case для получения кода верификации по ID"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)

    async def execute(
        self, id: int, force_delete: bool = False
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Получить код верификации по ID"""
        await self.validate(id=id, force_delete=force_delete)

        # Получение с relationships
        verification = await self.repository.get(
            id,
            options=self.repository.default_relationships(),
            include_deleted_filter=force_delete,
        )

        return UserCodeVerificationWithRelationsRDTO.model_validate(verification)

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """Валидация данных"""
        # Проверка существования
        verification = await self.repository.get(id, include_deleted_filter=force_delete)
        if not verification:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_code_verification_not_found")
            )

    async def transform(self, **kwargs) -> None:
        """Трансформация не требуется"""
        pass
