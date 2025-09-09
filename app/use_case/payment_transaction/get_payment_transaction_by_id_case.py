from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetPaymentTransactionByIdCase(BaseUseCase[PaymentTransactionRDTO]):
    """
    Класс Use Case для получения платежной транзакции по ID.

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.
        model (PaymentTransactionEntity | None): Найденная модель транзакции.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionRepository(db)
        self.model: PaymentTransactionEntity | None = None

    async def execute(self, id: int) -> PaymentTransactionRDTO:
        """
        Выполняет операцию получения платежной транзакции по ID.

        Args:
            id (int): ID транзакции для поиска.

        Returns:
            PaymentTransactionRDTO: Найденная платежная транзакция.
        """
        await self.validate(id=id)
        return PaymentTransactionRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска платежной транзакции по ID.

        Args:
            id (int): ID транзакции для валидации.

        Raises:
            AppExceptionResponse: Если транзакция не найдена.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))