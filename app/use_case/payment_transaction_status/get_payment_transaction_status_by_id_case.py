from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusRDTO
from app.adapters.repository.payment_transaction_status.payment_transaction_status_repository import PaymentTransactionStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetPaymentTransactionStatusByIdCase(BaseUseCase[PaymentTransactionStatusRDTO]):
    """
    Класс Use Case для получения статуса платежной транзакции по ID.

    Использует:
        - Репозиторий `PaymentTransactionStatusRepository` для работы с базой данных.
        - DTO `PaymentTransactionStatusRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionStatusRepository): Репозиторий для работы со статусами.
        model (PaymentTransactionStatusEntity | None): Найденная модель статуса.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionStatusRepository(db)
        self.model: PaymentTransactionStatusEntity | None = None

    async def execute(self, id: int) -> PaymentTransactionStatusRDTO:
        """
        Выполняет операцию получения статуса платежной транзакции по ID.

        Args:
            id (int): ID статуса для поиска.

        Returns:
            PaymentTransactionStatusRDTO: Найденный статус платежной транзакции.
        """
        await self.validate(id=id)
        return PaymentTransactionStatusRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидация поиска статуса платежной транзакции по ID.

        Args:
            id (int): ID статуса для валидации.

        Raises:
            AppExceptionResponse: Если статус не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))