from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestCDTO,
    BookingFieldPartyRequestWithRelationsRDTO
)
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateBookingFieldPartyRequestCase(BaseUseCase[BookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для создания бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyRequestRepository` для работы с базой данных
        - DTO `BookingFieldPartyRequestCDTO` для входных данных
        - DTO `BookingFieldPartyRequestWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyRequestRepository): Репозиторий для работы с бронированиями
        model (BookingFieldPartyRequestEntity | None): Модель бронирования для создания

    Методы:
        execute(dto: BookingFieldPartyRequestCDTO) -> BookingFieldPartyRequestWithRelationsRDTO:
            Создает новое бронирование и возвращает его с relationships
        validate(dto: BookingFieldPartyRequestCDTO):
            Валидирует данные для создания бронирования
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyRequestRepository(db)
        self.model: BookingFieldPartyRequestEntity | None = None

    async def execute(self, dto: BookingFieldPartyRequestCDTO) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Выполняет операцию создания бронирования площадки.

        Args:
            dto (BookingFieldPartyRequestCDTO): DTO с данными для создания бронирования

        Returns:
            BookingFieldPartyRequestWithRelationsRDTO: Созданное бронирование с relationships

        Raises:
            AppExceptionResponse: При ошибках валидации
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return BookingFieldPartyRequestWithRelationsRDTO.model_validate(model)

    async def validate(self, dto: BookingFieldPartyRequestCDTO) -> None:
        """
        Валидация данных для создания бронирования площадки.

        Проверяет:
        - Корректность дат (start_at < end_at)
        - Наличие хотя бы одного из: field_id или field_party_id

        Args:
            dto (BookingFieldPartyRequestCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если данные некорректны
        """
        # Проверка корректности дат бронирования
        if dto.start_at >= dto.end_at:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("start_date_must_be_before_end_date")
            )

        # Проверка наличия хотя бы одного из: field_id или field_party_id
        if not dto.field_id and not dto.field_party_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("either_field_or_field_party_required")
            )

        self.model = BookingFieldPartyRequestEntity(**dto.model_dump())