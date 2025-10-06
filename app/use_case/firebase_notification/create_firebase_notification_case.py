from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationCDTO,
    FirebaseNotificationWithRelationsRDTO,
)
from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.adapters.repository.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FirebaseNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateFirebaseNotificationCase(BaseUseCase[FirebaseNotificationWithRelationsRDTO]):
    """
    Use Case для создания Firebase уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model: FirebaseNotificationEntity | None = None

    async def execute(
        self, dto: FirebaseNotificationCDTO
    ) -> FirebaseNotificationWithRelationsRDTO:
        await self.validate(dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FirebaseNotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: FirebaseNotificationCDTO) -> None:
        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("user_not_found")
            )

        # Проверка уникальности токена для пользователя
        existed = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.user_id == dto.user_id,
                self.repository.model.token == dto.token,
            ]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("firebase_token_already_exists")
            )

        self.model = FirebaseNotificationEntity(**dto.dict())
