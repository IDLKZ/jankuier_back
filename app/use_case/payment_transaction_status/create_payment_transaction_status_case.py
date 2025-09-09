from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusCDTO, PaymentTransactionStatusRDTO
from app.adapters.repository.payment_transaction_status.payment_transaction_status_repository import PaymentTransactionStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreatePaymentTransactionStatusCase(BaseUseCase[PaymentTransactionStatusRDTO]):
    """
    Класс Use Case для создания статуса платежной транзакции.

    Использует:
        - Репозиторий `PaymentTransactionStatusRepository` для работы с базой данных.
        - DTO `PaymentTransactionStatusCDTO` для входных данных.
        - DTO `PaymentTransactionStatusRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionStatusRepository): Репозиторий для работы со статусами.
        model (PaymentTransactionStatusEntity | None): Модель статуса для создания.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionStatusRepository(db)
        self.model: PaymentTransactionStatusEntity | None = None

    async def execute(self, dto: PaymentTransactionStatusCDTO) -> PaymentTransactionStatusRDTO:
        """
        Выполняет операцию создания статуса платежной транзакции.

        Args:
            dto (PaymentTransactionStatusCDTO): DTO с данными для создания статуса.

        Returns:
            PaymentTransactionStatusRDTO: Созданный статус платежной транзакции.
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return PaymentTransactionStatusRDTO.from_orm(model)

    async def validate(self, dto: PaymentTransactionStatusCDTO) -> None:
        """
        Валидация данных для создания статуса платежной транзакции.

        Args:
            dto (PaymentTransactionStatusCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если статус с таким названием уже существует.
        """
        # Проверяем уникальность названия статуса
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.title_ru == dto.title_ru]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )
        
        self.model = PaymentTransactionStatusEntity(**dto.dict())