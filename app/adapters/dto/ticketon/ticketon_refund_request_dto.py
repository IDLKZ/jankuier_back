from pydantic import BaseModel

from app.shared.dto_constants import DTOConstant


class TicketonSaleRefundResponseDTO(BaseModel):
    status:DTOConstant.StandardIntegerField(description="1- успешно, 0 - ошибка")
    error:DTOConstant.StandardNullableTextField(description="Описание ошибки")
    code:DTOConstant.StandardNullableIntegerField(description="Код ошибки")