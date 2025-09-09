from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationPaymentTransactionWithRelationsRDTO
from app.adapters.filters.payment_transaction.payment_transaction_pagination_filter import PaymentTransactionPaginationFilter
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionWithRelationsRDTO


class PaginatePaymentTransactionCase(BaseUseCase[PaginationPaymentTransactionWithRelationsRDTO]):
    """
    Класс Use Case для пагинации платежных транзакций.

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationPaymentTransactionWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionRepository(db)

    async def execute(
        self, filter: PaymentTransactionPaginationFilter
    ) -> PaginationPaymentTransactionWithRelationsRDTO:
        """
        Выполняет операцию пагинации платежных транзакций.

        Args:
            filter (PaymentTransactionPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationPaymentTransactionWithRelationsRDTO: Пагинированный результат с транзакциями.
        """
        models = await self.repository.paginate(
            dto=PaymentTransactionWithRelationsRDTO,
            page=filter.page,
            per_page=filter.per_page,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return models

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass