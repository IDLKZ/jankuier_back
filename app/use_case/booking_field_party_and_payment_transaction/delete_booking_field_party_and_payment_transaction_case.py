from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import BookingFieldPartyAndPaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyAndPaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteBookingFieldPartyAndPaymentTransactionCase(BaseUseCase[bool]):
    """
    Use Case для удаления связи между бронированием площадки и платежной транзакцией.

    Используется для удаления связей когда:
    - Необходимо отменить/аннулировать связь между бронированием и транзакцией
    - Произошла ошибка при создании связи
    - Требуется очистка неактуальных связей

    Поддерживает два режима удаления:
    - Soft delete (по умолчанию): Устанавливает deleted_at, связь остается в БД
    - Hard delete: Полное удаление записи из базы данных

    Использует:
        - Repository `BookingFieldPartyAndPaymentTransactionRepository` для работы с базой данных

    Атрибуты:
        repository (BookingFieldPartyAndPaymentTransactionRepository): Репозиторий для работы со связями
        model (BookingFieldPartyAndPaymentTransactionEntity | None): Модель связи для удаления

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет связь (soft delete или force delete)
        validate(id: int):
            Валидирует существование связи перед удалением
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.repository = BookingFieldPartyAndPaymentTransactionRepository(db)
        self.model: BookingFieldPartyAndPaymentTransactionEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления связи между бронированием и транзакцией.

        Args:
            id (int): ID связи для удаления
            force_delete (bool): Флаг принудительного удаления (hard delete)
                                 False - soft delete (по умолчанию): устанавливает deleted_at
                                 True - полное удаление из БД (безвозвратно)

        Returns:
            bool: True если связь успешно удалена

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        await self.validate(id=id)
        return await self.repository.delete(id=id, force_delete=force_delete)

    async def validate(self, id: int) -> None:
        """
        Валидация перед удалением связи между бронированием и транзакцией.

        Проверяет существование связи (включая удаленные записи для возможности повторного удаления).

        Args:
            id (int): ID связи для валидации

        Raises:
            AppExceptionResponse: Если связь не найдена
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))