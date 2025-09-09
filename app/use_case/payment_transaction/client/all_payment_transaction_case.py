from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.filters.payment_transaction.payment_transaction_filter import PaymentTransactionFilter
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.use_case.base_case import BaseUseCase


class AllPaymentTransactionCase(BaseUseCase[list[PaymentTransactionRDTO]]):
    """
    Класс Use Case для получения списка платежных транзакций пользователя (клиентская версия).

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionRDTO` для возврата данных.
        
    Особенности:
        - Возвращает только транзакции конкретного пользователя.
        - Предназначен для использования клиентами для просмотра своих транзакций.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.

    Методы:
        execute() -> list[PaymentTransactionRDTO]:
            Выполняет запрос и возвращает список платежных транзакций пользователя.
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

    async def execute(self, filter: PaymentTransactionFilter, user_id: int) -> list[PaymentTransactionRDTO]:
        """
        Выполняет операцию получения списка платежных транзакций пользователя.

        Args:
            filter (PaymentTransactionFilter): Фильтр для дополнительной фильтрации.
            user_id (int): ID пользователя, чьи транзакции нужно получить.

        Returns:
            list[PaymentTransactionRDTO]: Список объектов платежных транзакций пользователя.
        """
        await self.validate(user_id=user_id)
        
        # Добавляем фильтр по пользователю к существующим фильтрам
        user_filters = filter.apply()
        user_filters.append(self.repository.model.user_id == user_id)
        
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=user_filters,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [PaymentTransactionRDTO.from_orm(model) for model in models]

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