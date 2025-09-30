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


class UpdateBookingFieldPartyRequestCase(BaseUseCase[BookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для обновления бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyRequestRepository` для работы с базой данных
        - DTO `BookingFieldPartyRequestCDTO` для входных данных
        - DTO `BookingFieldPartyRequestWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyRequestRepository): Репозиторий для работы с бронированиями
        model (BookingFieldPartyRequestEntity | None): Модель бронирования для обновления

    Методы:
        execute(id: int, dto: BookingFieldPartyRequestCDTO) -> BookingFieldPartyRequestWithRelationsRDTO:
            Обновляет бронирование и возвращает его с relationships
        validate(id: int, dto: BookingFieldPartyRequestCDTO):
            Валидирует существование бронирования и корректность данных
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyRequestRepository(db)
        self.model: BookingFieldPartyRequestEntity | None = None

    async def execute(self, id: int, dto: BookingFieldPartyRequestCDTO) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Выполняет операцию обновления бронирования площадки.

        Args:
            id (int): ID бронирования для обновления
            dto (BookingFieldPartyRequestCDTO): DTO с обновленными данными

        Returns:
            BookingFieldPartyRequestWithRelationsRDTO: Обновленное бронирование с relationships

        Raises:
            AppExceptionResponse: Если бронирование не найдено или данные некорректны
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return BookingFieldPartyRequestWithRelationsRDTO.model_validate(model)

    async def validate(self, id: int, dto: BookingFieldPartyRequestCDTO) -> None:
        """
        Валидация данных для обновления бронирования площадки.

        Проверяет:
        - Существование бронирования
        - Корректность дат (start_at < end_at)
        - Наличие хотя бы одного из: field_id или field_party_id

        Args:
            id (int): ID бронирования для валидации
            dto (BookingFieldPartyRequestCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если бронирование не найдено или данные некорректны
        """
        # Проверяем существование бронирования
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

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