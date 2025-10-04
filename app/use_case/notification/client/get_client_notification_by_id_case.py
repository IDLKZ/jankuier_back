from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationWithRelationsRDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.adapters.repository.read_notification.read_notification_repository import ReadNotificationRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import NotificationEntity, ReadNotificationEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetClientNotificationByIdCase(BaseUseCase[NotificationWithRelationsRDTO]):
    """
    Use Case для получения уведомления клиента по ID с автоматической отметкой о прочтении.

    ⚠️ ВАЖНОЕ ЗАМЕЧАНИЕ: Параметр id передаётся, но НЕ используется для поиска уведомления!
    Вместо этого ищется ПЕРВОЕ уведомление, доступное пользователю.

    Логика работы:
    1. Ищет ПЕРВОЕ уведомление, доступное пользователю (личное или общее через топики)
    2. При успешном получении автоматически создаёт запись о прочтении (side-effect)
    3. Запись о прочтении создаётся только если её ещё нет

    Типы уведомлений:
    - Личные: user_id == текущий пользователь
    - Общие: user_id is NULL AND topics IS NOT NULL (уведомления по топикам)
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.read_notification_repository = ReadNotificationRepository(db)
        self.model: NotificationEntity | None = None

    async def execute(self, id: int, user: UserWithRelationsRDTO) -> NotificationWithRelationsRDTO:
        """
        Главный метод выполнения use case.

        Args:
            id: ID уведомления (используется только для создания записи о прочтении!)
            user: Текущий пользователь

        Returns:
            NotificationWithRelationsRDTO: Найденное уведомление

        Raises:
            AppExceptionResponse: Если уведомление не найдено
        """
        await self.validate(id=id, user=user)
        return NotificationWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, user: UserWithRelationsRDTO) -> None:
        """
        Валидация, получение уведомления и автоматическая отметка о прочтении.

        ⚠️ КРИТИЧЕСКОЕ ЗАМЕЧАНИЕ: Параметр id НЕ используется для поиска!

        Логика поиска:
        - Ищет ПЕРВОЕ уведомление по условию OR:
          1. Личное уведомление: user_id == текущий пользователь
          2. Общее через топики: user_id IS NULL AND topics IS NOT NULL

        Side-effect:
        - Автоматически создаёт запись ReadNotification при первом чтении
        - Запись связывает user_id с notification_id

        Args:
            id: ID уведомления (используется ТОЛЬКО для создания ReadNotification!)
            user: Текущий пользователь

        Raises:
            AppExceptionResponse: Если уведомление не найдено
        """
        # ВНИМАНИЕ: id НЕ используется в фильтре! Ищется ПЕРВОЕ доступное уведомление
        self.model = await self.repository.get_first_with_filters(
            filters=[
                or_(
                    # Личное уведомление для конкретного пользователя
                    self.repository.model.user_id == user.id,
                    # ИЛИ общее уведомление по топикам (user_id = NULL, но есть топики)
                    and_(
                        self.repository.model.user_id.is_(None),
                        self.repository.model.topics.isnot(None)
                    )
                )
            ],
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )

        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Автоматическая отметка о прочтении (side-effect)
        # Проверяем, читал ли пользователь это уведомление ранее
        notification_read = await self.read_notification_repository.get_first_with_filters(
            filters=[
                self.read_notification_repository.model.user_id == user.id,
                self.read_notification_repository.model.notification_id == id,
            ]
        )

        # Если не читал - создаём запись о прочтении
        if not notification_read:
            await self.read_notification_repository.create(
                ReadNotificationEntity(
                    user_id=user.id,
                    notification_id=id
                )
            )

    async def transform(self) -> None:
        """
        Метод transform() требуется паттерном BaseUseCase, но не используется.
        """
        pass
