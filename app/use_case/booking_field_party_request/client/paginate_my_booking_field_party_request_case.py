from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import (
    BookingFieldPartyRequestWithRelationsRDTO
)
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyRequestWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.booking_field_party_request.booking_field_party_request_pagination_filter import (
    BookingFieldPartyRequestPaginationFilter
)
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import (
    BookingFieldPartyRequestRepository
)
from app.use_case.base_case import BaseUseCase


class PaginateMyBookingFieldPartyRequestCase(BaseUseCase[PaginationBookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка собственных заявок на бронирование.

    Возвращает только заявки, принадлежащие текущему пользователю.
    Поддерживает фильтрацию по различным параметрам и сортировку.

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
        filter: BookingFieldPartyRequestPaginationFilter,
        user: UserWithRelationsRDTO
    ) -> PaginationBookingFieldPartyRequestWithRelationsRDTO:
        """
        Получает пагинированный список собственных заявок на бронирование.

        Args:
            filter: Фильтр для пагинации с параметрами поиска и сортировки
            user: Текущий авторизованный пользователь

        Returns:
            PaginationBookingFieldPartyRequestWithRelationsRDTO: Пагинированный список заявок с relationships
        """
        # Добавляем фильтр по пользователю
        app_filter = filter.apply()
        app_filter.append(self.booking_field_party_request_repository.model.user_id == user.id)

        return await self.booking_field_party_request_repository.paginate(
            dto=BookingFieldPartyRequestWithRelationsRDTO,
            filters=app_filter,
            options=self.booking_field_party_request_repository.default_relationships(),
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
        )

    async def validate(self) -> None:
        """Валидация не требуется для данного use case."""
        pass
