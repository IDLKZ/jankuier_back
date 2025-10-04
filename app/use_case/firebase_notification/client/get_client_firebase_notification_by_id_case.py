from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.firebase_notification.firebase_notification_dto import (
    FirebaseNotificationWithRelationsRDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.firebase_notification.firebase_notification_repository import (
    FirebaseNotificationRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FirebaseNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetClientFirebaseNotificationByIdCase(BaseUseCase[FirebaseNotificationWithRelationsRDTO|None]):
    """
    Use Case для получения Firebase уведомления клиента.

    ВАЖНО: Несмотря на название "ByIdCase", данный use case получает ПЕРВОЕ уведомление
    пользователя, а не уведомление по конкретному ID. Параметр id в методах присутствует,
    но не используется в логике.

    Логика:
    - Ищет первое Firebase уведомление по user_id
    - Включает удалённые записи (include_deleted_filter=True)
    - Возвращает None, если уведомление не найдено
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = FirebaseNotificationRepository(db)
        self.model: FirebaseNotificationEntity | None = None

    async def execute(self,user: UserWithRelationsRDTO) -> FirebaseNotificationWithRelationsRDTO | None:
        """
        Главный метод выполнения use case.

        Args:
            id: ID уведомления (параметр передаётся, но НЕ используется в текущей логике)
            user: Текущий пользователь

        Returns:
            FirebaseNotificationWithRelationsRDTO | None: Найденное уведомление или None
        """
        await self.validate(user=user)
        if not self.model:
            return None
        return FirebaseNotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, user: UserWithRelationsRDTO) -> None:
        """
        Валидация и получение данных.

        ПРИМЕЧАНИЕ: Параметр id передаётся, но не используется!
        Вместо поиска по ID уведомления, выполняется поиск первого
        уведомления по user_id.

        Args:
            id: ID уведомления (не используется)
            user: Текущий пользователь
        """
        # ВНИМАНИЕ: Ищем первое уведомление пользователя, а НЕ по конкретному ID
        self.model = await self.repository.get_first_with_filters(
            filters=[
                self.repository.model.user_id == user.id,
            ],
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )

    async def transform(self) -> None:
        """
        Метод transform() требуется паттерном BaseUseCase, но не используется.
        """
        pass
