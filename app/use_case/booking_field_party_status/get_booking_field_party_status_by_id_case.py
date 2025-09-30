from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_status.booking_field_party_status_dto import BookingFieldPartyStatusWithRelationsRDTO
from app.adapters.repository.booking_field_party_status.booking_field_party_status_repository import BookingFieldPartyStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetBookingFieldPartyStatusByIdCase(BaseUseCase[BookingFieldPartyStatusWithRelationsRDTO]):
    """
    Use Case для получения статуса бронирования площадки по ID.

    Использует:
        - Repository `BookingFieldPartyStatusRepository` для работы с базой данных
        - DTO `BookingFieldPartyStatusWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyStatusRepository): Репозиторий для работы со статусами
        model (BookingFieldPartyStatusEntity | None): Найденная модель статуса

    Методы:
        execute(id: int) -> BookingFieldPartyStatusWithRelationsRDTO:
            Выполняет поиск статуса по ID и возвращает его с relationships
        validate(id: int):
            Валидирует существование статуса по ID
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyStatusRepository(db)
        self.model: BookingFieldPartyStatusEntity | None = None

    async def execute(self, id: int) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Выполняет операцию получения статуса бронирования площадки по ID.

        Args:
            id (int): ID статуса для поиска

        Returns:
            BookingFieldPartyStatusWithRelationsRDTO: Найденный статус с relationships

        Raises:
            AppExceptionResponse: Если статус не найден
        """
        await self.validate(id=id)
        return BookingFieldPartyStatusWithRelationsRDTO.model_validate(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска статуса бронирования площадки по ID.

        Args:
            id (int): ID статуса для валидации

        Raises:
            AppExceptionResponse: Если статус не найден
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))