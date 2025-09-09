from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetPaymentTransactionByIdCase(BaseUseCase[PaymentTransactionRDTO]):
    """
    Класс Use Case для получения платежной транзакции по ID (клиентская версия).

    Использует:
        - Репозиторий `PaymentTransactionRepository` для работы с базой данных.
        - DTO `PaymentTransactionRDTO` для возврата данных.
        
    Особенности:
        - Проверяет, что транзакция принадлежит запрашивающему пользователю.
        - Предназначен для использования клиентами для просмотра своих транзакций.

    Атрибуты:
        repository (PaymentTransactionRepository): Репозиторий для работы с транзакциями.
        model (PaymentTransactionEntity | None): Найденная модель транзакции.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionRepository(db)
        self.model: PaymentTransactionEntity | None = None

    async def execute(self, id: int, user_id: int) -> PaymentTransactionRDTO:
        """
        Выполняет операцию получения платежной транзакции по ID.

        Args:
            id (int): ID транзакции для поиска.
            user_id (int): ID пользователя, который запрашивает транзакцию.

        Returns:
            PaymentTransactionRDTO: Найденная платежная транзакция.

        Raises:
            AppExceptionResponse: Если транзакция не найдена или не принадлежит пользователю.
        """
        await self.validate(id=id, user_id=user_id)
        return PaymentTransactionRDTO.from_orm(self.model)

    async def validate(self, id: int, user_id: int) -> None:
        """
        Валидация поиска платежной транзакции по ID с проверкой владельца.

        Args:
            id (int): ID транзакции для валидации.
            user_id (int): ID пользователя для проверки владения.

        Raises:
            AppExceptionResponse: Если транзакция не найдена или не принадлежит пользователю.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
        
        # Проверяем, что транзакция принадлежит запрашивающему пользователю
        if self.model.user_id != user_id:
            raise AppExceptionResponse.forbidden(
                message=i18n.gettext("access_denied")
            )