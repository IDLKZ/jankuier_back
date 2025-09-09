from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.ticketon_order_status.ticketon_order_status_dto import TicketonOrderStatusRDTO
from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetTicketonOrderStatusByIdCase(BaseUseCase[TicketonOrderStatusRDTO]):
    """
    Класс Use Case для получения статуса заказа Ticketon по ID.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.
        - DTO `TicketonOrderStatusRDTO` для возврата данных.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.
        model (TicketonOrderStatusEntity | None): Найденная модель статуса.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderStatusRepository(db)
        self.model: TicketonOrderStatusEntity | None = None

    async def execute(self, id: int) -> TicketonOrderStatusRDTO:
        """
        Выполняет операцию получения статуса заказа Ticketon по ID.

        Args:
            id (int): ID статуса для поиска.

        Returns:
            TicketonOrderStatusRDTO: Найденный статус заказа Ticketon.
        """
        await self.validate(id=id)
        return TicketonOrderStatusRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска статуса заказа Ticketon по ID.

        Args:
            id (int): ID статуса для валидации.

        Raises:
            AppExceptionResponse: Если статус не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))