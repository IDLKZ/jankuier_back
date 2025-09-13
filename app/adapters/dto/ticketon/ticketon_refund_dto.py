from pydantic import BaseModel

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.shared.dto_constants import DTOConstant


class TicketonRefundDTO(BaseModel):
    payment_transaction: PaymentTransactionWithRelationsRDTO|None = None
    ticketon_order:TicketonOrderWithRelationsRDTO|None = None
    status:DTOConstant.StandardBooleanFalseField(description="Код результата") = False
    message:DTOConstant.StandardNullableTextField() = None