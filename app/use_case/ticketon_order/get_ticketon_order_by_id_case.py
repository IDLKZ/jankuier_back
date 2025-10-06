from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetTicketonOrderByIdCase(BaseUseCase[TicketonOrderRDTO]):
    """
    Класс Use Case для получения заказа Ticketon по ID.

    Использует:
        - Репозиторий `TicketonOrderRepository` для работы с базой данных.
        - DTO `TicketonOrderRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderRepository): Репозиторий для работы с заказами.
        model (TicketonOrderEntity | None): Найденная модель заказа.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderRepository(db)
        self.model: TicketonOrderEntity | None = None

    async def execute(self, id: int) -> TicketonOrderRDTO:
        """
        Выполняет операцию получения заказа Ticketon по ID.

        Args:
            id (int): ID заказа для поиска.

        Returns:
            TicketonOrderRDTO: Найденный заказ Ticketon.
        """
        await self.validate(id=id)
        return TicketonOrderRDTO.model_validate(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска заказа Ticketon по ID.

        Args:
            id (int): ID заказа для валидации.

        Raises:
            AppExceptionResponse: Если заказ не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))