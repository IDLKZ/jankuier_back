from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_status.booking_field_party_status_dto import (
    BookingFieldPartyStatusCDTO,
    BookingFieldPartyStatusWithRelationsRDTO
)
from app.adapters.repository.booking_field_party_status.booking_field_party_status_repository import BookingFieldPartyStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateBookingFieldPartyStatusCase(BaseUseCase[BookingFieldPartyStatusWithRelationsRDTO]):
    """
    Use Case для создания статуса бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyStatusRepository` для работы с базой данных
        - DTO `BookingFieldPartyStatusCDTO` для входных данных
        - DTO `BookingFieldPartyStatusWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyStatusRepository): Репозиторий для работы со статусами
        model (BookingFieldPartyStatusEntity | None): Модель статуса для создания

    Методы:
        execute(dto: BookingFieldPartyStatusCDTO) -> BookingFieldPartyStatusWithRelationsRDTO:
            Создает новый статус и возвращает его с relationships
        validate(dto: BookingFieldPartyStatusCDTO):
            Валидирует уникальность названия статуса
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyStatusRepository(db)
        self.model: BookingFieldPartyStatusEntity | None = None

    async def execute(self, dto: BookingFieldPartyStatusCDTO) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Выполняет операцию создания статуса бронирования площадки.

        Args:
            dto (BookingFieldPartyStatusCDTO): DTO с данными для создания статуса

        Returns:
            BookingFieldPartyStatusWithRelationsRDTO: Созданный статус с relationships

        Raises:
            AppExceptionResponse: Если статус с таким названием уже существует
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return BookingFieldPartyStatusWithRelationsRDTO.model_validate(model)

    async def validate(self, dto: BookingFieldPartyStatusCDTO) -> None:
        """
        Валидация данных для создания статуса бронирования площадки.

        Проверяет уникальность названия статуса на русском языке.

        Args:
            dto (BookingFieldPartyStatusCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если статус с таким названием уже существует
        """
        # Проверяем уникальность названия статуса
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.title_ru == dto.title_ru]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )

        self.model = BookingFieldPartyStatusEntity(**dto.model_dump())