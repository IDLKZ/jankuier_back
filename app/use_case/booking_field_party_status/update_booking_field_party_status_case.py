from sqlalchemy import and_
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


class UpdateBookingFieldPartyStatusCase(BaseUseCase[BookingFieldPartyStatusWithRelationsRDTO]):
    """
    Use Case для обновления статуса бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyStatusRepository` для работы с базой данных
        - DTO `BookingFieldPartyStatusCDTO` для входных данных
        - DTO `BookingFieldPartyStatusWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyStatusRepository): Репозиторий для работы со статусами
        model (BookingFieldPartyStatusEntity | None): Модель статуса для обновления

    Методы:
        execute(id: int, dto: BookingFieldPartyStatusCDTO) -> BookingFieldPartyStatusWithRelationsRDTO:
            Обновляет статус и возвращает его с relationships
        validate(id: int, dto: BookingFieldPartyStatusCDTO):
            Валидирует существование статуса и уникальность названия
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyStatusRepository(db)
        self.model: BookingFieldPartyStatusEntity | None = None

    async def execute(self, id: int, dto: BookingFieldPartyStatusCDTO) -> BookingFieldPartyStatusWithRelationsRDTO:
        """
        Выполняет операцию обновления статуса бронирования площадки.

        Args:
            id (int): ID статуса для обновления
            dto (BookingFieldPartyStatusCDTO): DTO с обновленными данными

        Returns:
            BookingFieldPartyStatusWithRelationsRDTO: Обновленный статус с relationships

        Raises:
            AppExceptionResponse: Если статус не найден или название уже используется
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return BookingFieldPartyStatusWithRelationsRDTO.model_validate(model)

    async def validate(self, id: int, dto: BookingFieldPartyStatusCDTO) -> None:
        """
        Валидация данных для обновления статуса бронирования площадки.

        Проверяет существование статуса и уникальность названия (исключая текущий статус).

        Args:
            id (int): ID статуса для валидации
            dto (BookingFieldPartyStatusCDTO): DTO с данными для валидации

        Raises:
            AppExceptionResponse: Если статус не найден или название уже используется
        """
        # Проверяем существование статуса
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверяем уникальность названия статуса (исключая текущий статус)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.title_ru == dto.title_ru,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )