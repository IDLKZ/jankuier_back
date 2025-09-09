from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.filters.payment_transaction.payment_transaction_filter import PaymentTransactionFilter
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.use_case.base_case import BaseUseCase


class AllPaymentTransactionCase(BaseUseCase[list[PaymentTransactionRDTO]]):
    """
    Класс Use Case для получения списка всех платежных транзакций.

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.

    Методы:
        execute() -> list[PaymentTransactionRDTO]:
            Выполняет запрос и возвращает список всех платежных транзакций.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = PaymentTransactionRepository(db)

    async def execute(self, filter: PaymentTransactionFilter) -> list[PaymentTransactionRDTO]:
        """
        Выполняет операцию получения списка всех платежных транзакций.

        Returns:
            list[PaymentTransactionRDTO]: Список объектов платежных транзакций.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [PaymentTransactionRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """