from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationWithRelationsRDTO,
)
from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FirebaseNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFirebaseNotificationByIdCase(BaseUseCase[FirebaseNotificationWithRelationsRDTO]):
    """
    Use Case для получения Firebase уведомления по ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.model: FirebaseNotificationEntity | None = None

    async def execute(self, id: int) -> FirebaseNotificationWithRelationsRDTO:
        await self.validate(id=id)
        return FirebaseNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
