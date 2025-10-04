from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import NotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteNotificationByIdCase(BaseUseCase[bool]):
    """
    Use Case для удаления уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.model: NotificationEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
