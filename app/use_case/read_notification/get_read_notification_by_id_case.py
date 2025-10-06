from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.read_notification.read_notification_dto import (
    ReadNotificationWithRelationsRDTO,
)
from app.adapters.repository.read_notification.read_notification_repository import (
    ReadNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ReadNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetReadNotificationByIdCase(BaseUseCase[ReadNotificationWithRelationsRDTO]):
    """
    Use Case для получения записи о прочитанном уведомлении по ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = ReadNotificationRepository(db)
        self.model: ReadNotificationEntity | None = None

    async def execute(self, id: int) -> ReadNotificationWithRelationsRDTO:
        await self.validate(id=id)
        return ReadNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
