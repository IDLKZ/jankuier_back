from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationTicketonOrderWithRelationsRDTO
from app.adapters.filters.ticketon_order.ticketon_order_pagination_filter import TicketonOrderPaginationFilter
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO


class PaginateTicketonOrderCase(BaseUseCase[PaginationTicketonOrderWithRelationsRDTO]):
    """
    Класс Use Case для пагинации заказов Ticketon пользователя (клиентская версия).

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationTicketonOrderWithRelationsRDTO` для пагинированного ответа.
        
    Особенности:
        - Возвращает только заказы конкретного пользователя с пагинацией.
        - Предназначен для использования клиентами для просмотра своих заказов.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderRepository(db)

    async def execute(
        self, filter: TicketonOrderPaginationFilter, user_id: int
    ) -> PaginationTicketonOrderWithRelationsRDTO:
        """
        Выполняет операцию пагинации заказов Ticketon пользователя.

        Args:
            filter (TicketonOrderPaginationFilter): Фильтр с параметрами пагинации.
            user_id (int): ID пользователя, чьи заказы нужно получить.

        Returns:
            PaginationTicketonOrderWithRelationsRDTO: Пагинированный результат с заказами пользователя.
        """
        await self.validate(user_id=user_id)
        
        # Добавляем фильтр по пользователю к существующим фильтрам
        user_filters = filter.apply()
        user_filters.append(self.repository.model.user_id == user_id)
        models = await self.repository.paginate(
            dto=TicketonOrderWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=user_filters,
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self, user_id: int) -> None:
        """
        Валидация перед выполнением.
        
        Args:
            user_id (int): ID пользователя для валидации.
        """
        # Здесь можно добавить дополнительные проверки, например:
        # - Проверка существования пользователя
        # - Проверка прав доступа
        if user_id is None:
            raise AppExceptionResponse.bad_request("User ID is required")