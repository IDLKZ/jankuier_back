from sqlalchemy import and_
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


class UpdateFirebaseNotificationCase(BaseUseCase[FirebaseNotificationWithRelationsRDTO]):
    """
    Use Case для обновления Firebase уведомления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.user_repository = UserRepository(db)
        self.model: FirebaseNotificationEntity | None = None

    async def execute(
        self, id: int, dto: FirebaseNotificationCDTO
    ) -> FirebaseNotificationWithRelationsRDTO:
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FirebaseNotificationWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: FirebaseNotificationCDTO) -> None:
        # Проверка существования записи
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка существования пользователя
        user = await self.user_repository.get(dto.user_id)
        if not user:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("user_not_found")
            )

        # Проверка уникальности токена для пользователя (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.user_id == dto.user_id,
                    self.repository.model.token == dto.token,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("firebase_token_already_exists")
            )
