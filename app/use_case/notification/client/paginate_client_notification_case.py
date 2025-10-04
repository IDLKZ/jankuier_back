from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.notification.notification_dto import (
    NotificationWithRelationsRDTO,
)
from app.adapters.dto.pagination_dto import PaginationNotificationWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.notification.notification_pagination_filter import (
    NotificationPaginationFilter,
)
from app.adapters.repository.notification.notification_repository import (
    NotificationRepository,
)
from app.adapters.repository.read_notification.read_notification_repository import ReadNotificationRepository
from app.use_case.base_case import BaseUseCase


class PaginateClientNotificationCase(BaseUseCase[PaginationNotificationWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка уведомлений клиента.

    Возвращает уведомления двух типов:
    1. Личные уведомления (user_id == текущий пользователь)
    2. Общие уведомления по топикам (user_id IS NULL AND topics IS NOT NULL)

    Поддерживает фильтрацию:
    - По статусу прочтения (is_read: true/false/null)
    - По поисковому запросу, сортировке и другим параметрам из NotificationPaginationFilter
    - По статусу удаления (is_show_deleted)
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = NotificationRepository(db)
        self.read_notification_repository = ReadNotificationRepository(db)

    async def execute(
        self, filter: NotificationPaginationFilter,
            user: UserWithRelationsRDTO
    ) -> PaginationNotificationWithRelationsRDTO:
        """
        Главный метод выполнения use case.

        Логика работы:
        1. Применяет базовые фильтры из NotificationPaginationFilter
        2. Добавляет фильтр доступа: только личные или общие через топики
        3. При наличии is_read фильтрует по статусу прочтения
        4. Возвращает пагинированный результат

        Args:
            filter: Фильтр пагинации с параметрами поиска и сортировки
            user: Текущий пользователь

        Returns:
            PaginationNotificationWithRelationsRDTO: Пагинированный список уведомлений
        """
        # Применяем базовые фильтры (поиск, сортировка и т.д.)
        all_filter = filter.apply()

        # Добавляем фильтр доступа к уведомлениям
        # Пользователь видит ЛИБО свои личные уведомления, ЛИБО общие по топикам
        all_filter.append(
            or_(
                # Личные уведомления для конкретного пользователя
                self.repository.model.user_id == user.id,
                # ИЛИ общие уведомления по топикам (без конкретного user_id)
                and_(
                    self.repository.model.user_id.is_(None),
                    self.repository.model.topics.isnot(None)
                )
            )
        )

        # Фильтрация по статусу прочтения (если указан параметр is_read)
        if filter.is_read is not None:
            notification_ids = []

            # Получаем все уведомления, которые пользователь уже прочитал
            notification_reads = await self.read_notification_repository.get_with_filters(
                filters=[
                    self.read_notification_repository.model.user_id == user.id,
                ]
            )

            # Собираем ID прочитанных уведомлений
            if notification_reads is not None:
                for notification_read in notification_reads:
                    notification_ids.append(notification_read.notification_id)

            # Применяем фильтр в зависимости от is_read
            if filter.is_read is True:
                # Показываем ТОЛЬКО прочитанные (ID в списке прочитанных)
                all_filter.append(self.repository.model.id.in_(notification_ids))
            else:
                # Показываем ТОЛЬКО непрочитанные (ID НЕ в списке прочитанных)
                all_filter.append(self.repository.model.id.notin_(notification_ids))

        # Выполняем пагинированный запрос с применёнными фильтрами
        models = await self.repository.paginate(
            dto=NotificationWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=all_filter,
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Метод validate() требуется паттерном BaseUseCase, но не используется.
        Валидация не требуется, так как все параметры валидируются на уровне фильтров.
        """
        pass

    async def transform(self) -> None:
        """
        Метод transform() требуется паттерном BaseUseCase, но не используется.
        """
        pass
