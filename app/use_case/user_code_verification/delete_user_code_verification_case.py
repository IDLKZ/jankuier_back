from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.user_code_verification_repository import (
    UserCodeVerificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteUserCodeVerificationCase(BaseUseCase[bool]):
    """Use case для удаления кода верификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserCodeVerificationRepository(db)

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """Удалить код верификации"""
        await self.validate(id=id)

        # Удаление
        return await self.repository.delete(id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """Валидация данных"""
        # Проверка существования
        verification = await self.repository.get(id, include_deleted_filter=True)
        if not verification:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_code_verification_not_found")
            )

    async def transform(self, **kwargs) -> None:
        """Трансформация не требуется"""
        pass
