from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon.ticketon_order_check_response_dto import (
    TicketonOrderCheckCommonResponseDTO,
    TicketonOrderCheckResponseDTO
)
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase


class CheckTicketonOrderCase(BaseUseCase[TicketonOrderCheckCommonResponseDTO]):
    """
    Use Case для проверки заказа Ticketon через API.

    Получает информацию о заказе из локальной БД и актуальную информацию
    о заказе из API Ticketon. Объединяет данные в общий ответ.

    Attributes:
        ticketon_repository: Репозиторий для работы с заказами Ticketon
        ticketon_service_api: API сервис для работы с Ticketon
        user: Текущий пользователь (опционально)
        ticket_order_id: ID заказа для проверки
        ticket_order_entity: Найденная сущность заказа
        order_check_dto: DTO с результатами проверки заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация use case для проверки заказа Ticketon.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.ticketon_repository = TicketonOrderRepository(db)
        self.ticketon_service_api = TicketonServiceAPI()
        self.user: UserWithRelationsRDTO | None = None
        self.ticket_order_id: int | None = None
        self.ticket_order_entity: TicketonOrderEntity | None = None
        self.order_check_dto: TicketonOrderCheckResponseDTO | None = None


    async def execute(
        self,
        ticketon_order_id: int,
        user: UserWithRelationsRDTO | None = None
    ) -> TicketonOrderCheckCommonResponseDTO:
        """
        Выполняет проверку заказа Ticketon.

        Получает заказ из локальной БД и проверяет его актуальный статус
        через API Ticketon. Возвращает объединенные данные.

        Args:
            ticketon_order_id: ID заказа для проверки
            user: Пользователь (для проверки прав доступа, опционально)

        Returns:
            TicketonOrderCheckCommonResponseDTO: Объединенные данные заказа и проверки

        Raises:
            AppExceptionResponse: При ошибке валидации или получения данных
        """
        self.user = user
        self.ticket_order_id = ticketon_order_id
        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация запроса на проверку заказа.

        Проверяет существование заказа в локальной БД.
        В будущем может добавиться проверка прав доступа пользователя.

        Raises:
            AppExceptionResponse: Если заказ не найден
        """
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

    async def transform(self) -> TicketonOrderCheckCommonResponseDTO:
        """
        Трансформация данных для ответа.

        Создает DTO с локальными данными заказа и результатами проверки
        через API Ticketon.

        Returns:
            TicketonOrderCheckCommonResponseDTO: Объединенные данные
        """
        # Создаем DTO для ответа
        result = TicketonOrderCheckCommonResponseDTO()

        # Добавляем локальные данные заказа
        result.ticketon_order = TicketonOrderWithRelationsRDTO.model_validate(
            self.ticket_order_entity
        )

        # Получаем актуальную информацию из API Ticketon
        if self.ticket_order_entity.sale:
            self.order_check_dto = await self.ticketon_service_api.check_order(
                self.ticket_order_entity.sale
            )
            result.order_check = self.order_check_dto

        return result

