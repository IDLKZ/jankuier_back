from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import UserEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteUserByIdCase(BaseUseCase[bool]):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = UserRepository(db)
        self.file_service = FileService(db)
        self.model: UserEntity | None = None
        self.file_id: int | None = None

    async def execute(self, id: int) -> bool:
        await self.validate(id=id)
        result = await self.repository.delete(id=id)
        if self.file_id and result:
            await self.file_service.delete_file(file_id=self.file_id)
        return result

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("user_not_found"))
        if self.model.image_id:
            self.file_id = self.model.image_id
