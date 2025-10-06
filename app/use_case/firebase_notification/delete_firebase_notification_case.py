from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FirebaseNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteFirebaseNotificationByIdCase(BaseUseCase[bool]):
    """
    Use Case для удаления Firebase уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.model: FirebaseNotificationEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
