from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon.ticketon_ticket_check_response_dto import (
    TicketonTicketCheckResponseDTO,
    TicketonTicketCheckCommonResponseDTO
)
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase


class CheckTicketonTicketCase(BaseUseCase[TicketonTicketCheckCommonResponseDTO]):
    """
    Use Case для проверки конкретного билета Ticketon через API.

    Проверяет существование билета в заказе и получает актуальную информацию
    о билете из API Ticketon. Объединяет данные в общий ответ.

    Attributes:
        ticketon_repository: Репозиторий для работы с заказами Ticketon
        ticketon_service_api: API сервис для работы с Ticketon
        user: Текущий пользователь (опционально)
        ticket_order_id: ID заказа, содержащего билет
        ticketon_ticket_id: ID билета для проверки
        ticket_order_entity: Найденная сущность заказа
        ticket_check_dto: DTO с результатами проверки билета
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация use case для проверки билета Ticketon.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.ticketon_repository = TicketonOrderRepository(db)
        self.ticketon_service_api = TicketonServiceAPI()
        self.user: UserWithRelationsRDTO | None = None
        self.ticket_order_id: int | None = None
        self.ticketon_ticket_id: str | None = None
        self.ticket_order_entity: TicketonOrderEntity | None = None
        self.ticket_check_dto: TicketonTicketCheckResponseDTO | None = None

    async def execute(
        self,
        ticketon_order_id: int,
        ticketon_ticket_id: str,
        user: UserWithRelationsRDTO | None = None
    ) -> TicketonTicketCheckCommonResponseDTO:
        """
        Выполняет проверку билета Ticketon.

        Проверяет существование билета в заказе и получает актуальную информацию
        о билете через API Ticketon. Возвращает объединенные данные.

        Args:
            ticketon_order_id: ID заказа, содержащего билет
            ticketon_ticket_id: ID билета для проверки
            user: Пользователь (для проверки прав доступа, опционально)

        Returns:
            TicketonTicketCheckCommonResponseDTO: Объединенные данные заказа и проверки билета

        Raises:
            AppExceptionResponse: При ошибке валидации или получения данных
        """
        self.user = user
        self.ticket_order_id = ticketon_order_id
        self.ticketon_ticket_id = ticketon_ticket_id
        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация запроса на проверку билета.

        Проверяет:
        1. Существование заказа в локальной БД
        2. Наличие билетов в заказе
        3. Существование конкретного билета в заказе

        Raises:
            AppExceptionResponse: При ошибке валидации
        """
        # Проверяем существование заказа
        self.ticket_order_entity = await self.ticketon_repository.get_first_with_filters(
            filters=[
                self.ticketon_repository.model.id == self.ticket_order_id,
                # TODO: Добавить проверку прав пользователя при необходимости
                # self.ticketon_repository.model.user_id == self.user.id
            ],
            include_deleted_filter=True,
            options=self.ticketon_repository.default_relationships()
        )
        if self.ticket_order_entity is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_order_not_found")
            )

        # Проверяем наличие билетов в заказе
        if not self.ticket_order_entity.tickets:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_order_tickets_not_found")
            )

        # Проверяем существование конкретного билета
        tickets = self.ticket_order_entity.tickets
        ticket_exists = any(
            ticket.get("id") == self.ticketon_ticket_id
            for ticket in tickets
        )
        if not ticket_exists:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticket_not_found")
            )

    async def transform(self) -> TicketonTicketCheckCommonResponseDTO:
        """
        Трансформация данных для ответа.

        Создает DTO с локальными данными заказа и результатами проверки
        конкретного билета через API Ticketon.

        Returns:
            TicketonTicketCheckCommonResponseDTO: Объединенные данные
        """
        # Создаем DTO для ответа
        result = TicketonTicketCheckCommonResponseDTO()

        # Добавляем локальные данные заказа
        result.ticketon_order = TicketonOrderWithRelationsRDTO.model_validate(
            self.ticket_order_entity
        )

        # Получаем актуальную информацию о билете из API Ticketon
        self.ticket_check_dto = await self.ticketon_service_api.check_ticket(
            self.ticketon_ticket_id
        )
        result.ticket_check = self.ticket_check_dto

        return result