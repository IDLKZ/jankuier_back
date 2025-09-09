from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusRDTO
from app.adapters.filters.ticketon_order_status.ticketon_order_status_filter import TicketonOrderStatusFilter
from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.use_case.base_case import BaseUseCase


class AllTicketonOrderStatusCase(BaseUseCase[list[TicketonOrderStatusRDTO]]):
    """
    Класс Use Case для получения списка всех статусов заказов Ticketon.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.
        - DTO `TicketonOrderStatusRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.

    Методы:
        execute() -> list[TicketonOrderStatusRDTO]:
            Выполняет запрос и возвращает список всех статусов заказов Ticketon.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = TicketonOrderStatusRepository(db)

    async def execute(self, filter: TicketonOrderStatusFilter) -> list[TicketonOrderStatusRDTO]:
        """
        Выполняет операцию получения списка всех статусов заказов Ticketon.

        Returns:
            list[TicketonOrderStatusRDTO]: Список объектов статусов заказов Ticketon.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [TicketonOrderStatusRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """