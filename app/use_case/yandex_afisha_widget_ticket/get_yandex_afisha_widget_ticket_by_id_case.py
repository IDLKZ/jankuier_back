from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_dto import (
    YandexAfishaWidgetTicketWithRelationsRDTO,
)
from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetYandexAfishaWidgetTicketByIdCase(
    BaseUseCase[YandexAfishaWidgetTicketWithRelationsRDTO]
):
    """
    Класс Use Case для получения билета Яндекс.Афиша по ID.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - DTO `YandexAfishaWidgetTicketWithRelationsRDTO` для возврата данных.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.

    Методы:
        execute() -> YandexAfishaWidgetTicketWithRelationsRDTO:
            Выполняет запрос и возвращает билет по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)

    async def execute(self, id: int) -> YandexAfishaWidgetTicketWithRelationsRDTO:
        """
        Выполняет операцию получения билета Яндекс.Афиша по ID.

        Args:
            id (int): ID билета.

        Returns:
            YandexAfishaWidgetTicketWithRelationsRDTO: Объект билета с связями.

        Raises:
            AppExceptionResponse: Если билет не найден.
        """
        await self.validate(id)

        model = await self.repository.get(
            id,
            include_deleted_filter=True,
            options=self.repository.default_relationships(),
        )
        if not model:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("yandex_afisha_widget_ticket_not_found")
            )

        return YandexAfishaWidgetTicketWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID билета для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("yandex_afisha_widget_ticket_id_validation_error")
            )
