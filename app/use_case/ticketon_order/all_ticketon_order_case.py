from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO
from app.adapters.filters.ticketon_order.ticketon_order_filter import TicketonOrderFilter
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.use_case.base_case import BaseUseCase


class AllTicketonOrderCase(BaseUseCase[list[TicketonOrderRDTO]]):
    """
    Класс Use Case для получения списка всех заказов Ticketon.

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.

    Методы:
        execute() -> list[TicketonOrderRDTO]:
            Выполняет запрос и возвращает список всех заказов Ticketon.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = TicketonOrderRepository(db)

    async def execute(self, filter: TicketonOrderFilter) -> list[TicketonOrderRDTO]:
        """
        Выполняет операцию получения списка всех заказов Ticketon.

        Returns:
            list[TicketonOrderRDTO]: Список объектов заказов Ticketon.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [TicketonOrderRDTO.model_validate(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """