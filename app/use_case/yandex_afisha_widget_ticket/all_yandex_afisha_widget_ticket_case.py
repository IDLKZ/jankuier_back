from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.filters.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_filter import (
    YandexAfishaWidgetTicketFilter,
)
from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.use_case.base_case import BaseUseCase


class AllYandexAfishaWidgetTicketCase(
    BaseUseCase[list[YandexAfishaWidgetTicketWithRelationsRDTO]]
):
    """
    Класс Use Case для получения списка всех билетов Яндекс.Афиша.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - DTO `YandexAfishaWidgetTicketWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.

    Методы:
        execute() -> list[YandexAfishaWidgetTicketWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех билетов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)

    async def execute(
        self, filter: YandexAfishaWidgetTicketFilter
    ) -> list[YandexAfishaWidgetTicketWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех билетов Яндекс.Афиша.

        По умолчанию возвращает только билеты с датой начала >= текущей даты.

        Args:
            filter (YandexAfishaWidgetTicketFilter): Фильтр для поиска и сортировки.

        Returns:
            list[YandexAfishaWidgetTicketWithRelationsRDTO]: Список объектов билетов с связями.
        """
        # Устанавливаем start_at_from по умолчанию на текущую дату, если не указан
        if filter.start_at_from is None:
            filter.start_at_from = datetime.now()

        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [
            YandexAfishaWidgetTicketWithRelationsRDTO.from_orm(model) for model in models
        ]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
