from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.read_notification.read_notification_dto import (
    ReadNotificationCDTO,
    ReadNotificationWithRelationsRDTO,
)
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.adapters.repository.read_notification.read_notification_repository import (
    ReadNotificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ReadNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateReadNotificationCase(BaseUseCase[ReadNotificationWithRelationsRDTO]):
    """
    Use Case для обновления записи о прочитанном уведомлении.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = ReadNotificationRepository(db)
        self.notification_repository = NotificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model: ReadNotificationEntity | None = None

    async def execute(
        self, id: int, dto: ReadNotificationCDTO
    ) -> ReadNotificationWithRelationsRDTO:
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return ReadNotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: ReadNotificationCDTO) -> None:
        # Проверка существования записи
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования уведомления
        notification = await self.notification_repository.get(dto.notification_id)
        if not notification:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("notification_not_found")
            )

        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("user_not_found")
            )

        # Проверка уникальности комбинации (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.notification_id == dto.notification_id,
                    self.repository.model.user_id == dto.user_id,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("notification_already_marked_as_read")
            )
