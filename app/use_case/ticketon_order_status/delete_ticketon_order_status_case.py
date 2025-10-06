from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.ticketon_order_status.ticketon_order_status_repository import TicketonOrderStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteTicketonOrderStatusCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления статуса заказа Ticketon.

    Использует:
        - Репозиторий `TicketonOrderStatusRepository` для работы с базой данных.

    Атрибуты:
        repository (TicketonOrderStatusRepository): Репозиторий для работы со статусами.
        model (TicketonOrderStatusEntity | None): Модель статуса для удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderStatusRepository(db)
        self.model: TicketonOrderStatusEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления статуса заказа Ticketon.

        Args:
            id (int): ID статуса для удаления.
            force_delete (bool): Флаг принудительного удаления.

        Returns:
            bool: True если статус успешно удален.
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидация перед удалением статуса заказа Ticketon.

        Args:
            id (int): ID статуса для валидации.

        Raises:
            AppExceptionResponse: Если статус не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))