from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusRDTO
from app.adapters.filters.payment_transaction_status.payment_transaction_status_filter import PaymentTransactionStatusFilter
from app.adapters.repository.payment_transaction_status.payment_transaction_status_repository import PaymentTransactionStatusRepository
from app.use_case.base_case import BaseUseCase


class AllPaymentTransactionStatusCase(BaseUseCase[list[PaymentTransactionStatusRDTO]]):
    """
    Класс Use Case для получения списка всех статусов платежных транзакций.

    Использует:
        - Репозиторий `PaymentTransactionStatusRepository` для работы с базой данных.
        - DTO `PaymentTransactionStatusRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionStatusRepository): Репозиторий для работы со статусами.

    Методы:
        execute() -> list[PaymentTransactionStatusRDTO]:
            Выполняет запрос и возвращает список всех статусов платежных транзакций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = PaymentTransactionStatusRepository(db)

    async def execute(self, filter: PaymentTransactionStatusFilter) -> list[PaymentTransactionStatusRDTO]:
        """
        Выполняет операцию получения списка всех статусов платежных транзакций.

        Returns:
            list[PaymentTransactionStatusRDTO]: Список объектов статусов платежных транзакций.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [PaymentTransactionStatusRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """