from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import BookingFieldPartyRequestWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationBookingFieldPartyRequestWithRelationsRDTO
from app.adapters.filters.booking_field_party_request.booking_field_party_request_pagination_filter import BookingFieldPartyRequestPaginationFilter
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.use_case.base_case import BaseUseCase


class PaginateBookingFieldPartyRequestCase(BaseUseCase[PaginationBookingFieldPartyRequestWithRelationsRDTO]):
    """
    Use Case для пагинации бронирований площадок.

    Использует:
        - Repository `BookingFieldPartyRequestRepository` для работы с базой данных
        - DTO `BookingFieldPartyRequestWithRelationsRDTO` для возврата данных с relationships
        - `PaginationBookingFieldPartyRequestWithRelationsRDTO` для пагинированного ответа

    Атрибуты:
        repository (BookingFieldPartyRequestRepository): Репозиторий для работы с бронированиями

    Методы:
        execute(filter: BookingFieldPartyRequestPaginationFilter) -> PaginationBookingFieldPartyRequestWithRelationsRDTO:
            Выполняет пагинацию бронирований с фильтрацией
        validate():
            Валидация (не используется в данном случае)
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyRequestRepository(db)

    async def execute(
        self, filter: BookingFieldPartyRequestPaginationFilter
    ) -> PaginationBookingFieldPartyRequestWithRelationsRDTO:
        """
        Выполняет операцию пагинации бронирований площадок.

        Args:
            filter (BookingFieldPartyRequestPaginationFilter): Фильтр с параметрами пагинации, поиска и сортировки

        Returns:
            PaginationBookingFieldPartyRequestWithRelationsRDTO: Пагинированный результат с бронированиями и relationships
        """
        models = await self.repository.paginate(
            dto=BookingFieldPartyRequestWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (не используется).
        """
        pass