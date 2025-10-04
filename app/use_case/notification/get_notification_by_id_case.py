from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationWithRelationsRDTO,
)
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import NotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetNotificationByIdCase(BaseUseCase[NotificationWithRelationsRDTO]):
    """
    Use Case для получения уведомления по ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.model: NotificationEntity | None = None

    async def execute(self, id: int) -> NotificationWithRelationsRDTO:
        await self.validate(id=id)
        return NotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
