from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import field_validator
from pydantic_xml import BaseXmlModel, element


class AlatauRefundOperationDTO(BaseXmlModel, tag='operation'):
    status: Optional[str] = element(default=None)
    result_desc: Optional[str] = element(default=None)
    result: Optional[int] = element(default=None)
    rc: Optional[str] = element(default=None)
    ecode: Optional[str] = element(default=None)
    edesc: Optional[str] = element(default=None)
    amount: Optional[Decimal] = element(default=None)
    rrn: Optional[str] = element(default=None)
    rev_desc: Optional[str] = element(default=None)
    rev_date: Optional[datetime] = element(default=None)

    @field_validator('rev_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                return None
        return v

    @field_validator('amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return Decimal(v)
            except (ValueError, TypeError):
                return None
        return v


class AlatauRefundPaymentResultDTO(BaseXmlModel, tag='result'):
    code: int = element()
    description: str = element()
    operation: Optional[AlatauRefundOperationDTO] = element(default=None)