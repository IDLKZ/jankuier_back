from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.auth.register_dto import UpdatePasswordDTO
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.core.auth_core import verify_password, get_password_hash
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdatePasswordCase(BaseUseCase[bool]):
    """
    Use case для обновления пароля пользователя.

    Атрибуты:
        repository (UserRepository): Репозиторий для работы с пользователями.
        user_id (int): ID пользователя для обновления пароля.
        model: Модель пользователя.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.user_id: int | None = None
        self.model = None

    async def execute(self, user_id: int, dto: UpdatePasswordDTO) -> bool:
        self.user_id = user_id
        await self.validate(dto)
        await self.transform(dto)

        # Обновляем пароль
        new_password_hash = get_password_hash(dto.new_password)
        self.model.password_hash = new_password_hash
        await self.repository.db.commit()
        await self.repository.db.refresh(self.model)

        return True

    async def validate(self, dto: UpdatePasswordDTO) -> None:
        # Проверяем, что пользователь существует
        self.model = await self.repository.get(id=self.user_id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("user_not_found")
            )

        # Проверяем старый пароль
        if not verify_password(dto.old_password, self.model.password_hash):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_old_password")
            )

        # Проверяем, что новый пароль отличается от старого
        if dto.old_password == dto.new_password:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("new_password_must_be_different")
            )

    async def transform(self, dto: UpdatePasswordDTO) -> None:
        # Дополнительная обработка данных при необходимости
        pass