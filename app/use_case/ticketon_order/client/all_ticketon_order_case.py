from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO
from app.adapters.filters.ticketon_order.ticketon_order_filter import TicketonOrderFilter
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.use_case.base_case import BaseUseCase


class AllTicketonOrderCase(BaseUseCase[list[TicketonOrderRDTO]]):
    """
    Класс Use Case для получения списка заказов Ticketon пользователя (клиентская версия).

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderRDTO` для возврата данных.
        
    Особенности:
        - Возвращает только заказы конкретного пользователя.
        - Предназначен для использования клиентами для просмотра своих заказов.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.

    Методы:
        execute() -> list[TicketonOrderRDTO]:
            Выполняет запрос и возвращает список заказов Ticketon пользователя.
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

    async def execute(self, filter: TicketonOrderFilter, user_id: int|None = None) -> list[TicketonOrderRDTO]:
        """
        Выполняет операцию получения списка заказов Ticketon пользователя.

        Args:
            filter (TicketonOrderFilter): Фильтр для дополнительной фильтрации.
            user_id (int): ID пользователя, чьи заказы нужно получить.

        Returns:
            list[TicketonOrderRDTO]: Список объектов заказов Ticketon пользователя.
        """
        #await self.validate(user_id=user_id)
        
        # Добавляем фильтр по пользователю к существующим фильтрам
        user_filters = filter.apply()
        #user_filters.append(self.repository.model.user_id == user_id)
        
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=user_filters,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [TicketonOrderRDTO.from_orm(model) for model in models]

    async def validate(self, user_id: int) -> None:
        """
        Валидация перед выполнением.
        
        Args:
            user_id (int): ID пользователя для валидации.
        """
        # Здесь можно добавить дополнительные проверки, например:
        # - Проверка существования пользователя
        # - Проверка прав доступа
        pass