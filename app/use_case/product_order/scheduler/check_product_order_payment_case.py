import datetime
import traceback
from typing import List, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionCDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO, ProductOrderCDTO, \
    ProductOrderRDTO
from app.adapters.repository.payment_transaction.payment_transaction_repository import PaymentTransactionRepository
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_and_payment_transaction.product_order_and_payment_transaction_repository import \
    ProductOrderAndPaymentTransactionRepository
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase, T


class CheckProductOrderPaymentCase(BaseUseCase[List[ProductOrderRDTO]]):

    def __init__(self, db: AsyncSession) -> None:
        self.product_order_repository = ProductOrderRepository(db)
        self.payment_repository = PaymentTransactionRepository(db)
        self.product_order_and_payment_repository = ProductOrderAndPaymentTransactionRepository(db)
        self.now = None



    async def execute(self) -> List[ProductOrderRDTO]:
        try:
            self.now = datetime.datetime.now()
            product_orders = await self.product_order_repository.get_with_filters(
                filters=[
                    self.product_order_repository.model.paid_until < self.now,
                    self.product_order_repository.model.status_id == DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID
                ],
                options=self.product_order_repository.default_relationships(),
                include_deleted_filter=True
            )
            order_ids = []
            for order_item in product_orders:
                order = ProductOrderCDTO.from_orm(order_item)
                order.status_id = DbValueConstants.ProductOrderStatusCancelledID
                order.is_canceled = True
                order.is_paid = False
                order.is_active = False
                order.cancel_reason = "Оплата просрочена"
                order_ids.append(order_item.id)
                await self.product_order_repository.update(order_item,order)

            if order_ids:
                relations = await self.product_order_and_payment_repository.get_with_filters(
                    filters=[
                        self.product_order_and_payment_repository.model.product_order_id.in_(order_ids)
                    ],
                    options=self.product_order_and_payment_repository.default_relationships(),
                )
                if relations:
                    for relation in relations:
                        payment_transaction_cdto = PaymentTransactionCDTO.from_orm(relation.payment_transaction)
                        payment_transaction_cdto.is_paid = False
                        payment_transaction_cdto.is_active = False
                        payment_transaction_cdto.status_id = DbValueConstants.PaymentTransactionStatusCancelledID
                        await self.payment_repository.update(relation.payment_transaction, payment_transaction_cdto)
                return [ProductOrderRDTO.model_validate(order) for order in product_orders]
        except Exception as exc:
            traceback.print_exc()

    async def validate(self, *args: Any, **kwargs: Any):
        pass
