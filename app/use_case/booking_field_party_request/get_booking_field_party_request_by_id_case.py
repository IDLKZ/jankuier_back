from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import BookingFieldPartyRequestWithRelationsRDTO
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetBookingFieldPartyRequestByIdCase(BaseUseCase[BookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для получения бронирования площадки по ID.

    Использует:
        - Repository `BookingFieldPartyRequestRepository` для работы с базой данных
        - DTO `BookingFieldPartyRequestWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyRequestRepository): Репозиторий для работы с бронированиями
        model (BookingFieldPartyRequestEntity | None): Найденная модель бронирования

    Методы:
        execute(id: int) -> BookingFieldPartyRequestWithRelationsRDTO:
            Выполняет поиск бронирования по ID и возвращает его с relationships
        validate(id: int):
            Валидирует существование бронирования по ID
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyRequestRepository(db)
        self.model: BookingFieldPartyRequestEntity | None = None

    async def execute(self, id: int) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Выполняет операцию получения бронирования площадки по ID.

        Args:
            id (int): ID бронирования для поиска

        Returns:
            BookingFieldPartyRequestWithRelationsRDTO: Найденное бронирование с relationships

        Raises:
            AppExceptionResponse: Если бронирование не найдено
        """
        await self.validate(id=id)
        return BookingFieldPartyRequestWithRelationsRDTO.model_validate(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска бронирования площадки по ID.

        Args:
            id (int): ID бронирования для валидации

        Raises:
            AppExceptionResponse: Если бронирование не найдено
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))