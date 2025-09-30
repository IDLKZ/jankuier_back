from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_status.booking_field_party_status_dto import BookingFieldPartyStatusWithRelationsRDTO
from app.adapters.filters.booking_field_party_status.booking_field_party_status_filter import BookingFieldPartyStatusFilter
from app.adapters.repository.booking_field_party_status.booking_field_party_status_repository import BookingFieldPartyStatusRepository
from app.use_case.base_case import BaseUseCase


class AllBookingFieldPartyStatusCase(BaseUseCase[list[BookingFieldPartyStatusWithRelationsRDTO]]):
    """
    Use Case для получения списка всех статусов бронирования площадок.

    Использует:
        - Repository `BookingFieldPartyStatusRepository` для работы с базой данных
        - DTO `BookingFieldPartyStatusWithRelationsRDTO` для возврата данных с relationships

    Атрибуты:
        repository (BookingFieldPartyStatusRepository): Репозиторий для работы со статусами

    Методы:
        execute(filter: BookingFieldPartyStatusFilter) -> list[BookingFieldPartyStatusWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех статусов с relationships
        validate():
            Метод валидации (не используется в данном случае)
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyStatusRepository(db)

    async def execute(self, filter: BookingFieldPartyStatusFilter) -> list[BookingFieldPartyStatusWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех статусов бронирования площадок.

        Args:
            filter (BookingFieldPartyStatusFilter): Фильтр для поиска и сортировки

        Returns:
            list[BookingFieldPartyStatusWithRelationsRDTO]: Список статусов с relationships
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [BookingFieldPartyStatusWithRelationsRDTO.model_validate(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (не используется).
        """
        pass