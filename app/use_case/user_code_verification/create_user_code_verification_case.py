from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.user_code_verification.user_code_verification_dto import (
    UserCodeVerificationCDTO,
    UserCodeVerificationWithRelationsRDTO,
)
from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities.user_code_verification_entity import UserCodeVerificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateUserCodeVerificationCase(
    BaseUseCase[UserCodeVerificationWithRelationsRDTO]
):
    """Use case для создания кода верификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)
        self.user_repository = UserRepository(db)

    async def execute(
        self, dto: UserCodeVerificationCDTO
    ) -> UserCodeVerificationWithRelationsRDTO:
        """Создать код верификации"""
        await self.validate(dto=dto)
        dto = await self.transform(dto=dto)

        # Создание entity
        entity = UserCodeVerificationEntity(**dto.model_dump())
        created_entity = await self.repository.create(entity)

        # Получение с relationships
        verification = await self.repository.get(
            created_entity.id,
            options=self.repository.default_relationships(),
        )

        return UserCodeVerificationWithRelationsRDTO.model_validate(verification)

    async def validate(self, dto: UserCodeVerificationCDTO) -> None:
        """Валидация данных"""
        # Проверка существования пользователя
        if dto.user_id:
            user = await self.user_repository.get(dto.user_id)
            if not user:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("user_not_found")
                )

    async def transform(self, dto: UserCodeVerificationCDTO) -> UserCodeVerificationCDTO:
        """Трансформация данных"""
        return dto
