from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationUDTO,
    UserCodeVerificationWithRelationsRDTO,
)
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateUserCodeVerificationCase(
    BaseUseCase[UserCodeVerificationWithRelationsRDTO]
):
    """Use case для обновления кода верификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model = None

    async def execute(
        self, id: int, dto: UserCodeVerificationUDTO
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Обновить код верификации"""
        await self.validate(id=id, dto=dto)
        dto = await self.transform(dto=dto)

        # Обновление
        updated_entity = await self.repository.update(self.model, dto)

        # Получение с relationships
        verification = await self.repository.get(
            updated_entity.id,
            options=self.repository.default_relationships(),
        )

        return UserCodeVerificationWithRelationsRDTO.model_validate(verification)

    async def validate(self, id: int, dto: UserCodeVerificationUDTO) -> None:
        """Валидация данных"""
        # Проверка существования кода верификации
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_code_verification_not_found")
            )

        # Проверка существования пользователя (если изменяется)
        if dto.user_id:
            user = await self.user_repository.get(dto.user_id)
            if not user:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("user_not_found")
                )

    async def transform(
        self, dto: UserCodeVerificationUDTO
    ) -> UserCodeVerificationUDTO:
        """Трансформация данных"""
        return dto
