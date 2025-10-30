from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationYandexAfishaWidgetTicketWithRelationsRDTO
from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.filters.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_pagination_filter import (
    YandexAfishaWidgetTicketPaginationFilter,
)
from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.use_case.base_case import BaseUseCase


class PaginateYandexAfishaWidgetTicketCase(
    BaseUseCase[PaginationYandexAfishaWidgetTicketWithRelationsRDTO]
):
    """
    Класс Use Case для получения билетов Яндекс.Афиша с пагинацией.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - DTO `YandexAfishaWidgetTicketWithRelationsRDTO` для возврата данных с связями.
        - `PaginationYandexAfishaWidgetTicketWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.

    Методы:
        execute() -> PaginationYandexAfishaWidgetTicketWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список билетов.
        validate():
            Метод валидации (пока пустой).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)

    async def execute(
        self, filter: YandexAfishaWidgetTicketPaginationFilter
    ) -> PaginationYandexAfishaWidgetTicketWithRelationsRDTO:
        """
        Выполняет операцию получения билетов Яндекс.Афиша с пагинацией.

        По умолчанию возвращает только билеты с датой начала >= текущей даты.

        Args:
            filter (YandexAfishaWidgetTicketPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationYandexAfishaWidgetTicketWithRelationsRDTO: Пагинированный список билетов с связями.
        """
        # Устанавливаем start_at_from по умолчанию на текущую дату, если не указан
        if filter.start_at_from is None:
            filter.start_at_from = datetime.now()

        models = await self.repository.paginate(
            dto=YandexAfishaWidgetTicketWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
