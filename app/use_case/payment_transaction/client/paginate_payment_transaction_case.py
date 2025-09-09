from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationPaymentTransactionWithRelationsRDTO
from app.adapters.filters.payment_transaction.payment_transaction_pagination_filter import PaymentTransactionPaginationFilter
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionWithRelationsRDTO


class PaginatePaymentTransactionCase(BaseUseCase[PaginationPaymentTransactionWithRelationsRDTO]):
    """
    Класс Use Case для пагинации платежных транзакций пользователя (клиентская версия).

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationPaymentTransactionWithRelationsRDTO` для пагинированного ответа.
        
    Особенности:
        - Возвращает только транзакции конкретного пользователя с пагинацией.
        - Предназначен для использования клиентами для просмотра своих транзакций.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionRepository(db)

    async def execute(
        self, filter: PaymentTransactionPaginationFilter, user_id: int
    ) -> PaginationPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию пагинации платежных транзакций пользователя.

        Args:
            filter (PaymentTransactionPaginationFilter): Фильтр с параметрами пагинации.
            user_id (int): ID пользователя, чьи транзакции нужно получить.

        Returns:
            PaginationPaymentTransactionWithRelationsRDTO: Пагинированный результат с транзакциями пользователя.
        """
        await self.validate(user_id=user_id)
        
        # Добавляем фильтр по пользователю к существующим фильтрам
        user_filters = filter.apply()
        user_filters.append(self.repository.model.user_id == user_id)
        
        models = await self.repository.paginate(
            dto=PaymentTransactionWithRelationsRDTO,
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
        pass