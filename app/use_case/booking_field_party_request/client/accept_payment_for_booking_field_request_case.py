import datetime
import traceback
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefGetDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_create_request_dto import \
    AcceptPaymentForBookingFieldPartyResponseDTO
from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import BookingFieldPartyRequestCDTO, \
    BookingFieldPartyRequestWithRelationsRDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionRDTO
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import \
    BookingFieldPartyAndPaymentTransactionRepository
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import \
    BookingFieldPartyRequestRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import BookingFieldPartyRequestEntity, PaymentTransactionEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase, T


class AcceptPaymentForBookingFieldRequestCase(BaseUseCase[AcceptPaymentForBookingFieldPartyResponseDTO]):
    """
    Use Case для обработки callback от платежной системы Alatau после оплаты бронирования.

    Процесс включает:
    1. Проверку цифровой подписи от платежной системы
    2. Поиск платежной транзакции по номеру заказа
    3. Поиск связанной заявки на бронирование
    4. Обновление статуса платежной транзакции
    5. Обновление статуса заявки на бронирование (если оплата успешна)

    Используется:
    - Платежной системой Alatau для уведомления о результате оплаты (BACKREF URL)
    - Не требует авторизации пользователя (проверка через цифровую подпись)

    Attributes:
        booking_field_party_request_repository: Репозиторий для работы с заявками на бронирование
        payment_transaction_repository: Репозиторий для работы с платежными транзакциями
        booking_field_party_and_payment_transaction_repository: Репозиторий для связей между заявками и транзакциями
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.booking_field_party_request_repository = BookingFieldPartyRequestRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.booking_field_party_and_payment_transaction_repository = BookingFieldPartyAndPaymentTransactionRepository(db)

        self.dto:AlatauBackrefGetDTO|None = None
        self.should_update:bool = False
        self.paid:bool = False
        self.current_booking_field_party_request:BookingFieldPartyRequestEntity|None = None
        self.current_payment_transaction:PaymentTransactionEntity|None = None
        self.response:AcceptPaymentForBookingFieldPartyResponseDTO = AcceptPaymentForBookingFieldPartyResponseDTO()


    async def execute(self, dto: AlatauBackrefGetDTO) -> AcceptPaymentForBookingFieldPartyResponseDTO:
        """
        Обрабатывает callback от платежной системы и обновляет статусы заявки и транзакции.

        Args:
            dto: DTO с данными от платежной системы (номер заказа, код результата, подпись)

        Returns:
            AcceptPaymentForBookingFieldPartyResponseDTO: Ответ с обновленной заявкой и транзакцией

        Raises:
            AppExceptionResponse.bad_request: Если подпись невалидна, транзакция или заявка не найдены
        """
        self.dto = dto
        await self.validate()
        await self.transform()
        self.response.field_booking_request = BookingFieldPartyRequestWithRelationsRDTO.from_orm(self.current_booking_field_party_request)
        self.response.payment_transaction = PaymentTransactionRDTO.from_orm(self.current_payment_transaction)
        self.response.is_success = self.paid
        return self.response


    async def validate(self) -> None:
        """
        Валидирует callback от платежной системы и находит связанные сущности.

        Проверяет:
        - Наличие данных от платежной системы
        - Корректность цифровой подписи (безопасность)
        - Существование платежной транзакции по номеру заказа
        - Существование связи между транзакцией и заявкой
        - Существование заявки на бронирование
        - Определяет, нужно ли обновлять статус заявки (res_code == "0" и статус "Ожидание оплаты")

        Raises:
            AppExceptionResponse.bad_request: При невалидной подписи или отсутствии связанных данных
        """
        if not self.dto:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("no_data"))

        if self.dto.verify_signature(app_config.shared_secret) is False:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("invalid_signature"))

        self.current_payment_transaction = await self.payment_transaction_repository.get_first_with_filters(
            filters=[self.payment_transaction_repository.model.order == self.dto.order],
            include_deleted_filter=True,
        )
        if not self.current_payment_transaction:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))

        payment_and_request = await self.booking_field_party_and_payment_transaction_repository.get_first_with_filters(
            filters=[
                self.booking_field_party_and_payment_transaction_repository.model.payment_transaction_id == self.current_payment_transaction.id,
            ]
        )
        if not payment_and_request:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("payment_transaction_not_found"))

        self.current_booking_field_party_request = await self.booking_field_party_request_repository.get_first_with_filters(
            filters=[self.booking_field_party_request_repository.model.id == payment_and_request.request_id],
            include_deleted_filter=True,
            options=self.booking_field_party_request_repository.default_relationships()
        )
        if not self.current_booking_field_party_request:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("booking_field_party_request_not_found"))

        if self.dto.res_code == "0" and self.current_booking_field_party_request.status_id == DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentID:
            self.should_update = True

        if self.dto.res_code == "0":
            self.paid = True

        self.response.message = self.dto.res_desc


    async def transform(self) -> None:
        """
        Обновляет статусы платежной транзакции и заявки на бронирование.

        Выполняет следующие шаги:
        1. Обновляет платежную транзакцию:
           - Сохраняет данные от платежной системы (mpi_order, res_code, res_desc, sign)
           - Устанавливает is_active = False (транзакция завершена)
           - Устанавливает статус "Оплачено" (если res_code == "0") или "Ошибка"
        2. Обновляет заявку на бронирование (только если оплата успешна):
           - Устанавливает статус "Оплачено"
           - Сохраняет ID транзакции и номер заказа
           - Устанавливает is_paid = True и время оплаты

        В случае ошибки логирует исключение в response.message.
        """
        try:
            # Обновляем транзакцию
            payment_transaction_cdto = PaymentTransactionCDTO.from_orm(self.current_payment_transaction)
            payment_transaction_cdto.mpi_order = self.dto.mpi_order
            payment_transaction_cdto.res_desc = self.dto.res_desc
            payment_transaction_cdto.res_code = self.dto.res_code
            payment_transaction_cdto.paid_p_sign = self.dto.sign
            payment_transaction_cdto.is_active = False
            payment_transaction_cdto.is_paid = self.paid
            if self.paid:
                payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusPaidID
            else:
                payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusFailedID
            self.current_payment_transaction = await self.payment_transaction_repository.update(
                obj=self.current_payment_transaction,
                dto=payment_transaction_cdto
            )
            self.current_payment_transaction = await self.payment_transaction_repository.get(
                self.current_payment_transaction.id,
                include_deleted_filter=True,
            )

            # Обновляем заявку (только при успешной оплате)
            if self.should_update and self.paid:
                booking_field_party_request_cdto = BookingFieldPartyRequestCDTO.from_orm(
                    self.current_booking_field_party_request)
                booking_field_party_request_cdto.status_id = DbValueConstants.BookingFieldPartyStatusPaidID
                booking_field_party_request_cdto.payment_transaction_id = self.current_payment_transaction.id
                booking_field_party_request_cdto.paid_order = self.dto.order
                booking_field_party_request_cdto.is_paid = True
                booking_field_party_request_cdto.paid_at = datetime.datetime.now()
                self.current_booking_field_party_request = await self.booking_field_party_request_repository.update(
                    obj=self.current_booking_field_party_request,
                    dto=booking_field_party_request_cdto
                )
                self.current_booking_field_party_request = await self.booking_field_party_request_repository.get(
                    self.current_booking_field_party_request.id,
                    include_deleted_filter=True,
                    options=self.booking_field_party_request_repository.default_relationships()
                )
        except Exception:
            self.response.message = traceback.format_exc()

