from datetime import timedelta, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_create_order_dto import AlatauCreateResponseOrderDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO, PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingShowBookingDTO, TicketonBookingRequestDTO, \
    TicketonBookingErrorResponseDTO
from app.adapters.dto.ticketon.ticketon_response_for_sale_dto import TicketonResponseForSaleDTO
from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO, TicketonOrderCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import TicketonOrderEntity, PaymentTransactionEntity
from app.helpers.alatau_helper import AlatauHelper
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.infrastructure.service.alatau_service.alatau_service_api import AlatauServiceAPI
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.db_constants import DbColumnConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateSaleTicketonAndOrderCase(BaseUseCase[TicketonResponseForSaleDTO]):

    def __init__(self, db: AsyncSession) -> None:
        self.ticketon_repository = TicketonOrderRepository(db)
        self.payment_transaction_repository = PaymentTransactionRepository(db)
        self.ticketon_service_api = TicketonServiceAPI()
        self.alatau_service_api = AlatauServiceAPI()
        self.ticketon_booking_result: TicketonBookingShowBookingDTO | None = None
        self.ticketon_request_dto: TicketonBookingRequestDTO | None = None
        self.user: UserWithRelationsRDTO | None = None
        self.current_time: datetime | None = None
        self.ticketon_order_entity: TicketonOrderEntity | None = None
        self.payment_transaction_entity: PaymentTransactionEntity | None = None
        self.order_dto = AlatauCreateResponseOrderDTO()
        self.common_response_dto = TicketonResponseForSaleDTO()

    async def execute(self, dto: TicketonBookingRequestDTO, user: UserWithRelationsRDTO | None = None) -> TicketonResponseForSaleDTO:
        self.user = user
        self.ticketon_request_dto = dto
        await self.validate()
        await self.transform()
        await self.create_transaction()
        return self.common_response_dto



    async def validate(self) -> None:
        if not self.ticketon_request_dto:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("booking_request_required"))
        
        if not self.ticketon_request_dto.email:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("email_required"))
            
        if not self.ticketon_request_dto.phone:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("phone_required"))
        
        self.ticketon_booking_result = await self.ticketon_service_api.sale_ticketon(self.ticketon_request_dto)
        if isinstance(self.ticketon_booking_result, TicketonBookingErrorResponseDTO):
            raise AppExceptionResponse.bad_request(message=self.ticketon_booking_result.error)
        
        if not self.ticketon_booking_result.sale:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("sale_id_required"))
            
        self.current_time = datetime.now()

    async def transform(self) -> None:
        try:
            cdto = TicketonOrderCDTO(
                user_id=self.user.id if self.user else None,
                status_id=DbValueConstants.TicketonOrderStatusBookingCreatedID,
                seats=self.ticketon_booking_result.seats,
                show=self.ticketon_booking_result.show,
                sale=self.ticketon_booking_result.sale,
                lang=self.ticketon_booking_result.lang,
                pre_sale=self.ticketon_booking_result.sale,
                reservation_id=self.ticketon_booking_result.reservation_id,
                price=self.ticketon_booking_result.price,
                expire=self.ticketon_booking_result.expire,
                expired_at=self.current_time + timedelta(seconds=self.ticketon_booking_result.expire),
                sum=self.ticketon_booking_result.sum,
                currency=self.ticketon_booking_result.currency,
                pre_tickets=[ticket.dict() if hasattr(ticket, 'dict') else ticket for ticket in self.ticketon_booking_result.tickets] if self.ticketon_booking_result.tickets else None,
                tickets=[ticket.dict() if hasattr(ticket, 'dict') else ticket for ticket in self.ticketon_booking_result.tickets] if self.ticketon_booking_result.tickets else None,
                sale_secury_token=self.ticketon_booking_result.sale_secury_token,
                is_active=True,
                is_paid=False,
                is_canceled=False,
                cancel_reason=None,
                email=self.ticketon_request_dto.email,
                phone=self.ticketon_request_dto.phone,
            )
            self.ticketon_order_entity = await self.ticketon_repository.create(TicketonOrderEntity(**cdto.dict()))
            self.common_response_dto.ticketon = self.ticketon_booking_result
        except Exception as e:
            if self.ticketon_booking_result and self.ticketon_booking_result.sale:
                try:
                    await self.ticketon_service_api.sale_cancel(self.ticketon_booking_result.sale)
                except Exception:
                    pass
            raise AppExceptionResponse.internal_error(
                message=f"{i18n.gettext('ticket_sale_error')}: {str(e)}"
            ) from e



    async def create_transaction(self) -> None:
        try:
            show: TicketonSingleShowResponseDTO | None = await TicketonServiceAPI().get_ticketon_single_show(
                int(self.ticketon_booking_result.show), use_cache=True
            )
            
            self.order_dto.ORDER = self.ticketon_booking_result.sale
            self.order_dto.AMOUNT = self.ticketon_booking_result.sum
            self.order_dto.DESC = "Покупка билетов на мероприятие"
            self.order_dto.DESC_ORDER = AlatauHelper.make_desc(self.ticketon_booking_result, show)
            self.order_dto.EMAIL = self.ticketon_request_dto.email
            self.order_dto.PHONE = self.ticketon_request_dto.phone
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
                email=self.ticketon_request_dto.email,
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
            
            self.payment_transaction_entity = await self.payment_transaction_repository.create(
                PaymentTransactionEntity(**payment_cdto.dict())
            )
            
            # Link ticketon order with payment transaction
            # Set response data
            self.common_response_dto.order = self.order_dto.dict()
            self.common_response_dto.payment_transaction_id = self.payment_transaction_entity.id
            
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
        
        # 2. Удаляем ticketon_order если был создан
        if self.ticketon_order_entity:
            try:
                await self.ticketon_repository.delete(
                    self.ticketon_order_entity.id, 
                    force_delete=True
                )
                print(f"✅ Ticketon order {self.ticketon_order_entity.id} deleted after error")
            except Exception as e:
                cleanup_errors.append(f"Failed to delete ticketon_order: {str(e)}")
                print(f"❌ Failed to delete ticketon_order: {str(e)}")
        
        # 3. Отменяем sale в Ticketon API если была создана
        if self.ticketon_booking_result and self.ticketon_booking_result.sale:
            try:
                await self.ticketon_service_api.sale_cancel(self.ticketon_booking_result.sale)
            except Exception as e:
                cleanup_errors.append(f"Failed to cancel Ticketon sale: {str(e)}")
