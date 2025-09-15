from datetime import timedelta, datetime
from decimal import Decimal
from typing import Any
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingShowBookingDTO
from app.adapters.dto.ticketon.ticketon_response_for_sale_dto import TicketonResponseForSaleDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import PaymentTransactionEntity
from app.helpers.alatau_helper import AlatauHelper
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.alatau_service.alatau_service_api import AlatauServiceAPI
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class RecreatePaymentForTicketonOrderCase(BaseUseCase[TicketonResponseForSaleDTO]):
    """
    Use case для восстановления/пересоздания платежа для существующего заказа Ticketon.
    
    Логика:
    1. Находит заказ Ticketon по ID
    2. Ищет активную payment_transaction для этого заказа
    3. Если активная найдена - возвращает её данные
    4. Если не найдена - создает новую payment_transaction
    5. Возвращает TicketonResponseForSaleDTO с данными для оплаты
    """

    def __init__(self, db: AsyncSession) -> None:
        self.ticketon_repository = TicketonOrderRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.alatau_service_api = AlatauServiceAPI()
        self.ticketon_service_api = TicketonServiceAPI()
        self.ticketon_booking_result: TicketonBookingShowBookingDTO | None = None
        self.ticketon_order: TicketonOrderWithRelationsRDTO | None = None
        self.active_payment_transaction: PaymentTransactionEntity | None = None
        self.payment_transaction_entity: PaymentTransactionEntity | None = None
        self.order_dto = AlatauCreateResponseOrderDTO()
        self.common_response_dto = TicketonResponseForSaleDTO()
        self.current_time = datetime.now()
        self.user: UserWithRelationsRDTO | None = None


    async def execute(self, ticketon_order_id: int,user:UserWithRelationsRDTO|None = None) -> TicketonResponseForSaleDTO:
        """
        Выполняет восстановление/пересоздание платежа для заказа Ticketon.
        
        Args:
            ticketon_order_id: ID заказа Ticketon
            
        Returns:
            TicketonResponseForSaleDTO с данными для оплаты
        """
        self.user = user
        await self.validate(ticketon_order_id)
        await self.transform()
        return self.common_response_dto

    async def validate(self, ticketon_order_id: int) -> None:
        self.ticketon_order = await self.ticketon_repository.get_first_with_filters(
            filters=[
                self.ticketon_repository.model.id == ticketon_order_id,
            ],
            include_deleted_filter=True
        )
        if not self.ticketon_order:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_not_found"))

        if self.ticketon_order.is_active is False or self.ticketon_order.is_canceled is True:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_not_active"))

        if self.ticketon_order.is_paid is True:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_already_paid"))
        if self.ticketon_order.expired_at < self.current_time and self.ticketon_order.is_active is True:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("ticketon_order_is_expired"))
        self.ticketon_booking_result = TicketonBookingShowBookingDTO.from_orm(self.ticketon_order)
        self.common_response_dto.ticketon = self.ticketon_booking_result

        self.active_payment_transaction = await self.payment_transaction_repository.get_first_with_filters(
            filters=[
                self.payment_transaction_repository.model.order == self.ticketon_order.sale,
                self.payment_transaction_repository.model.transaction_type == DbValueConstants.PaymentTicketonType,
                self.payment_transaction_repository.model.is_active.is_(True),
                self.payment_transaction_repository.model.is_canceled.is_(False),
                self.payment_transaction_repository.model.is_paid.is_(False),
            ],
            include_deleted_filter=True
        )
        if not self.active_payment_transaction:
            await self.create_transaction()
        else:
            self.order_dto.ORDER = self.active_payment_transaction.order
            self.order_dto.AMOUNT = self.active_payment_transaction.amount
            self.order_dto.DESC = self.active_payment_transaction.desc
            self.order_dto.DESC_ORDER = self.active_payment_transaction.desc_order
            self.order_dto.EMAIL = self.active_payment_transaction.email
            # Note: PHONE не используется в AlatauCreateResponseOrderDTO для платежной системы
            self.order_dto.NONCE = self.active_payment_transaction.nonce
            self.order_dto.CLIENT_ID = self.active_payment_transaction.client_id
            self.order_dto.NAME = self.active_payment_transaction.name
            self.order_dto.P_SIGN = self.active_payment_transaction.pre_p_sign

        self.common_response_dto.order = self.order_dto.dict()
        self.common_response_dto.payment_transaction_id = self.active_payment_transaction.id

    async def transform(self) -> None:
        """
        Обрабатывает данные и создает/находит payment_transaction.
        """

    async def create_transaction(self) -> None:
        try:
            show: TicketonSingleShowResponseDTO | None = await TicketonServiceAPI().get_ticketon_single_show(
                int(self.ticketon_booking_result.show), use_cache=True
            )

            self.order_dto.ORDER = self.ticketon_booking_result.sale
            self.order_dto.AMOUNT = self.ticketon_booking_result.sum
            self.order_dto.DESC = "Покупка билетов на мероприятие"
            self.order_dto.DESC_ORDER = AlatauHelper.make_desc(self.ticketon_booking_result, show)
            self.order_dto.EMAIL = self.ticketon_order.email
            # Note: PHONE не используется в AlatauCreateResponseOrderDTO для платежной системы
            self.order_dto.NONCE = await self.payment_transaction_repository.generate_unique_noncense()

            if self.user:
                self.order_dto.CLIENT_ID = self.user.id
                self.order_dto.NAME = f"{self.user.first_name or ''} {self.user.last_name or ''}".strip()

            self.order_dto.set_signature(self.alatau_service_api.shared_token)

            # Create payment transaction
            payment_cdto = PaymentTransactionCDTO(
                user_id=self.user.id if self.user else None,
                status_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                transaction_type=DbValueConstants.PaymentTicketonType,
                order=self.ticketon_booking_result.sale,
                nonce=self.order_dto.NONCE,
                amount=self.ticketon_booking_result.sum,
                currency=self.ticketon_booking_result.currency or "KZT",
                merchant=app_config.merchant_id,
                language="ru",
                client_id=self.user.id if self.user else None,
                desc="Покупка билетов на мероприятие",
                desc_order=self.order_dto.DESC_ORDER,
                email=self.ticketon_order.email,
                name=self.order_dto.NAME if hasattr(self.order_dto, 'NAME') else None,
                pre_p_sign=self.order_dto.P_SIGN,
                is_active=True,
                is_paid=False,
                is_canceled=False,
                expired_at=self.current_time + timedelta(seconds=self.ticketon_booking_result.expire),
                order_full_info={
                    "ticketon_booking": self.ticketon_booking_result.dict(),
                    "alatau_order": self.order_dto.dict(),
                    "show_info": show.dict() if show else None,
                }
            )

            self.active_payment_transaction = await self.payment_transaction_repository.create(
                PaymentTransactionEntity(**payment_cdto.dict())
            )
            # Для корректной очистки при ошибках
            self.payment_transaction_entity = self.active_payment_transaction

        except Exception as e:
            # Полная очистка при ошибке эквайринга
            await self._cleanup_after_error(str(e))

            # Выбрасываем понятную ошибку пользователю
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("acquiring_error_try_again"),
                extra={
                    "error_type": "acquiring_error",
                    "original_error": str(e),
                    "action": "retry"
                }
            ) from e

    async def _cleanup_after_error(self, error_message: str) -> None:
        """
        Выполняет полную очистку созданных данных при ошибке в create_transaction.

        Порядок очистки:
        1. Удаляет payment_transaction (если была создана)
        2. Удаляет ticketon_order (если был создан)
        3. Отменяет sale в Ticketon API (если была создана)

        Args:
            error_message: Сообщение об ошибке для логирования
        """
        cleanup_errors = []

        # 1. Удаляем payment_transaction если была создана
        if self.payment_transaction_entity:
            try:
                await self.payment_transaction_repository.delete(
                    self.payment_transaction_entity.id,
                    force_delete=True
                )
                print(f"✅ Payment transaction {self.payment_transaction_entity.id} deleted after error")
            except Exception as e:
                cleanup_errors.append(f"Failed to delete payment_transaction: {str(e)}")
                print(f"❌ Failed to delete payment_transaction: {str(e)}")

        # 2. В RecreatePaymentCase мы НЕ создаем ticketon_order, он уже существует
        # Поэтому не удаляем его при ошибке
        print("ℹ️ Ticketon order существовал до вызова, не удаляем при ошибке")

        # 3. В RecreatePaymentCase мы НЕ создаем sale, он уже существует 
        # Поэтому не отменяем его при ошибке создания payment_transaction
        print("ℹ️ Ticketon sale существовал до вызова, не отменяем при ошибке")