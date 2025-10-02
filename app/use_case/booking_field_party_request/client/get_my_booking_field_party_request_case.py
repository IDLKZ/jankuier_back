from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestWithRelationsRDTO
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import (
    BookingFieldPartyRequestRepository
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetMyBookingFieldPartyRequestCase(BaseUseCase[BookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для получения собственной заявки на бронирование по ID.

    Проверяет, что заявка принадлежит текущему пользователю.
    Возвращает заявку со всеми связанными данными (relationships).

    Attributes:
        booking_field_party_request_repository: Репозиторий для работы с заявками на бронирование
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.booking_field_party_request_repository = BookingFieldPartyRequestRepository(db)

    async def execute(
        self,
        id: int,
        user: UserWithRelationsRDTO
    ) -> BookingFieldPartyRequestWithRelationsRDTO:
        """
        Получает собственную заявку на бронирование по ID.

        Args:
            id: ID заявки на бронирование
            user: Текущий авторизованный пользователь

        Returns:
            BookingFieldPartyRequestWithRelationsRDTO: Заявка со всеми relationships

        Raises:
            AppExceptionResponse.not_found: Если заявка не найдена или не принадлежит пользователю
        """
        booking_request = await self.booking_field_party_request_repository.get_first_with_filters(
            filters=[
                self.booking_field_party_request_repository.model.id == id,
                self.booking_field_party_request_repository.model.user_id == user.id
            ],
            options=self.booking_field_party_request_repository.default_relationships()
        )

        if not booking_request:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("booking_field_party_request_not_found")
            )

        return BookingFieldPartyRequestWithRelationsRDTO.from_orm(booking_request)

    async def validate(self) -> None:
        """Валидация не требуется для данного use case."""
        pass
