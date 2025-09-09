from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction_status.payment_transaction_status_dto import PaymentTransactionStatusRDTO, PaymentTransactionStatusCDTO
from app.adapters.repository.payment_transaction_status.payment_transaction_status_repository import PaymentTransactionStatusRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionStatusEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdatePaymentTransactionStatusCase(BaseUseCase[PaymentTransactionStatusRDTO]):
    """
    Класс Use Case для обновления статуса платежной транзакции.

    Использует:
        - Репозиторий `PaymentTransactionStatusRepository` для работы с базой данных.
        - DTO `PaymentTransactionStatusCDTO` для входных данных.
        - DTO `PaymentTransactionStatusRDTO` для возврата данных.

    Атрибуты:
        repository (PaymentTransactionStatusRepository): Репозиторий для работы со статусами.
        model (PaymentTransactionStatusEntity | None): Модель статуса для обновления.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.repository = PaymentTransactionStatusRepository(db)
        self.model: PaymentTransactionStatusEntity | None = None

    async def execute(self, id: int, dto: PaymentTransactionStatusCDTO) -> PaymentTransactionStatusRDTO:
        """
        Выполняет операцию обновления статуса платежной транзакции.

        Args:
            id (int): ID статуса для обновления.
            dto (PaymentTransactionStatusCDTO): DTO с обновленными данными.

        Returns:
            PaymentTransactionStatusRDTO: Обновленный статус платежной транзакции.
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return PaymentTransactionStatusRDTO.from_orm(model)

    async def validate(self, id: int, dto: PaymentTransactionStatusCDTO) -> None:
        """
        Валидация данных для обновления статуса платежной транзакции.

        Args:
            id (int): ID статуса для валидации.
            dto (PaymentTransactionStatusCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если статус не найден или название уже используется.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
        
        # Проверяем уникальность названия статуса (исключая текущий статус)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.title_ru == dto.title_ru,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.title_ru}"
            )