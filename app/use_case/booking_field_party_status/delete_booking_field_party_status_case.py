from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.booking_field_party_status.booking_field_party_status_repository import BookingFieldPartyStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteBookingFieldPartyStatusCase(BaseUseCase[bool]):
    """
    Use Case для удаления статуса бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyStatusRepository` для работы с базой данных

    Атрибуты:
        repository (BookingFieldPartyStatusRepository): Репозиторий для работы со статусами
        model (BookingFieldPartyStatusEntity | None): Модель статуса для удаления

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет статус (soft delete или force delete)
        validate(id: int):
            Валидирует существование статуса перед удалением
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyStatusRepository(db)
        self.model: BookingFieldPartyStatusEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления статуса бронирования площадки.

        Args:
            id (int): ID статуса для удаления
            force_delete (bool): Флаг принудительного удаления (hard delete)
                                 False - soft delete (по умолчанию)
                                 True - полное удаление из БД

        Returns:
            bool: True если статус успешно удален

        Raises:
            AppExceptionResponse: Если статус не найден
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидация перед удалением статуса бронирования площадки.

        Проверяет существование статуса.

        Args:
            id (int): ID статуса для валидации

        Raises:
            AppExceptionResponse: Если статус не найден
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))