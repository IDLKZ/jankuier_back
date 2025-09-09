from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationPaymentTransactionStatusWithRelationsRDTO
from app.adapters.filters.payment_transaction_status.payment_transaction_status_pagination_filter import PaymentTransactionStatusPaginationFilter
from app.adapters.repository.payment_transaction_status.payment_transaction_status_repository import PaymentTransactionStatusRepository
from app.use_case.base_case import BaseUseCase
from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusWithRelationsRDTO


class PaginatePaymentTransactionStatusCase(BaseUseCase[PaginationPaymentTransactionStatusWithRelationsRDTO]):
    """
    Класс Use Case для пагинации статусов платежных транзакций.

    Использует:
        - Репозиторий `PaymentTransactionStatusRepository` для работы с базой данных.
        - DTO `PaymentTransactionStatusWithRelationsRDTO` для возврата данных с отношениями.
        - `PaginationPaymentTransactionStatusWithRelationsRDTO` для пагинированного ответа.

    Атрибуты:
        repository (PaymentTransactionStatusRepository): Репозиторий для работы со статусами.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionStatusRepository(db)

    async def execute(
        self, filter: PaymentTransactionStatusPaginationFilter
    ) -> PaginationPaymentTransactionStatusWithRelationsRDTO:
        """
        Выполняет операцию пагинации статусов платежных транзакций.

        Args:
            filter (PaymentTransactionStatusPaginationFilter): Фильтр с параметрами пагинации.

        Returns:
            PaginationPaymentTransactionStatusWithRelationsRDTO: Пагинированный результат со статусами.
        """
        models = await self.repository.paginate(
            dto=PaymentTransactionStatusWithRelationsRDTO,
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