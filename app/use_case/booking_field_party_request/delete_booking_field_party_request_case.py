from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import BookingFieldPartyRequestRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteBookingFieldPartyRequestCase(BaseUseCase[bool]):
    """
    Use Case для удаления бронирования площадки.

    Использует:
        - Repository `BookingFieldPartyRequestRepository` для работы с базой данных

    Атрибуты:
        repository (BookingFieldPartyRequestRepository): Репозиторий для работы с бронированиями
        model (BookingFieldPartyRequestEntity | None): Модель бронирования для удаления

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет бронирование (soft delete или force delete)
        validate(id: int):
            Валидирует существование бронирования перед удалением
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyRequestRepository(db)
        self.model: BookingFieldPartyRequestEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления бронирования площадки.

        Args:
            id (int): ID бронирования для удаления
            force_delete (bool): Флаг принудительного удаления (hard delete)
                                 False - soft delete (по умолчанию)
                                 True - полное удаление из БД

        Returns:
            bool: True если бронирование успешно удалено

        Raises:
            AppExceptionResponse: Если бронирование не найдено
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидация перед удалением бронирования площадки.

        Проверяет существование бронирования.

        Args:
            id (int): ID бронирования для валидации

        Raises:
            AppExceptionResponse: Если бронирование не найдено
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))