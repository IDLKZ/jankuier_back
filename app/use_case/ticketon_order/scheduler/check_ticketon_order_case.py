import traceback
from datetime import datetime
from typing import List, Any

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.booking_field_party_request.booking_field_party_request_dto import BookingFieldPartyRequestRDTO, \
    BookingFieldPartyRequestCDTO
from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderRDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderRDTO, TicketonOrderCDTO
from app.adapters.repository.booking_field_party_and_payment_transaction.booking_field_party_and_payment_transaction_repository import \
    BookingFieldPartyAndPaymentTransactionRepository
from app.adapters.repository.booking_field_party_request.booking_field_party_request_repository import \
    BookingFieldPartyRequestRepository
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.ticketon_order.ticketon_order_repository import TicketonOrderRepository
from app.adapters.repository.ticketon_order_and_payment_transaction.ticketon_order_and_payment_transaction_repository import \
    TicketonOrderAndPaymentTransactionRepository
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CheckTicketonOrderTimeCase(BaseUseCase[List[TicketonOrderRDTO]]):

    def __init__(self, db: AsyncSession) -> None:
        self.repository = TicketonOrderRepository(db)
        self.payment_repository = PaymentTransactionRepository(db)
        self.ticketon_order_and_payment_transaction_repository = TicketonOrderAndPaymentTransactionRepository(db)
        self.ticketonService = TicketonServiceAPI()
        self.now = None

    async def execute(self) -> List[TicketonOrderRDTO]:
        try:
            self.now = datetime.now()
            orders = await self.repository.get_with_filters(
                filters=[
                    self.repository.model.expired_at < self.now,
                    self.repository.model.status_id == DbValueConstants.TicketonOrderStatusBookingCreatedID
                ],
                options=self.repository.default_relationships(),
                include_deleted_filter=True
            )
            order_ids = []
            for order_item in orders:
                order = TicketonOrderCDTO.from_orm(order_item)
                order.status_id = DbValueConstants.TicketonOrderStatusCancelledID
                order.is_canceled = True
                order.is_paid = False
                order.is_active = False
                order.cancel_reason = "Оплата просрочена"
                order_ids.append(order_item.id)
                await self.repository.update(order_item,order)
                try:
                    if order_item.sale:
                        await self.ticketonService.sale_cancel(order_item.sale)
                except Exception as exc:
                    traceback.print_exc()

            if order_ids:
                relations = await self.ticketon_order_and_payment_transaction_repository.get_with_filters(
                    filters=[
                        self.ticketon_order_and_payment_transaction_repository.model.ticketon_order_id.in_(order_ids)
                    ],
                    options=self.ticketon_order_and_payment_transaction_repository.default_relationships(),
                )
                if relations:
                    for relation in relations:
                        payment_transaction_cdto = PaymentTransactionCDTO.from_orm(relation.payment_transaction)
                        payment_transaction_cdto.is_paid = False
                        payment_transaction_cdto.is_active = False
                        payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusCancelledID
                        await self.payment_repository.update(relation.payment_transaction, payment_transaction_cdto)
                return [ProductOrderRDTO.model_validate(order) for order in orders]

        except Exception as exc:
            traceback.print_exc()

    async def validate(self, *args: Any, **kwargs: Any):
        pass

