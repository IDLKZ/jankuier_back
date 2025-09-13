from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import field_validator
from pydantic_xml import BaseXmlModel, element


class RefundRecordDTO(BaseXmlModel, tag='rec'):
    status: Optional[str] = element(default=None)
    status_desc: Optional[str] = element(default=None)
    rev_rc: Optional[str] = element(default=None)
    rev_amount: Optional[Decimal] = element(default=None)
    rev_description: Optional[str] = element(default=None)
    rev_error: Optional[str] = element(default=None)
    rev_date: Optional[datetime] = element(default=None)
    ecode: Optional[str] = element(default=None)
    edesc: Optional[str] = element(default=None)

    @field_validator('rev_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                return None
        return v

    @field_validator('rev_amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return Decimal(v)
            except (ValueError, TypeError):
                return None
        return v


class RefundsDTO(BaseXmlModel, tag='refunds'):
    records: List[RefundRecordDTO] = element(tag='rec', default_factory=list)


class AlatauOperationDTO(BaseXmlModel, tag='operation'):
    status: Optional[str] = element(default=None)
    status_desc: Optional[str] = element(default=None)
    amount: Optional[Decimal] = element(default=None)
    currency: Optional[str] = element(default=None)
    description: Optional[str] = element(default=None)
    desc_order: Optional[str] = element(default=None)
    email: Optional[str] = element(default=None)
    phone: Optional[str] = element(default=None)
    lang: Optional[str] = element(default=None)
    mpi_order: Optional[str] = element(default=None)
    terminal: Optional[str] = element(default=None)
    create_date: Optional[datetime] = element(default=None)
    card_masked: Optional[str] = element(default=None)
    card_name: Optional[str] = element(default=None)
    card_expdt: Optional[str] = element(default=None)
    card_token: Optional[str] = element(default=None)
    result: Optional[int] = element(default=None)
    result_desc: Optional[str] = element(default=None)
    rc: Optional[str] = element(default=None)
    rrn: Optional[str] = element(default=None)
    int_ref: Optional[str] = element(default=None)
    auth_code: Optional[str] = element(default=None)
    inv_id: Optional[str] = element(default=None)
    inv_exp_date: Optional[str] = element(default=None)
    rev_max_amount: Optional[Decimal] = element(default=None)
    recur_freq: Optional[str] = element(default=None)
    requr_exp: Optional[str] = element(default=None)
    recur_ref: Optional[str] = element(default=None)
    recur_int_ref: Optional[str] = element(default=None)
    client_id: Optional[str] = element(default=None)
    card_to_masked: Optional[str] = element(default=None)
    cart_to_token: Optional[str] = element(default=None)
    fee: Optional[Decimal] = element(default=None)
    ecode: Optional[str] = element(default=None)
    edesc: Optional[str] = element(default=None)
    merch_rn_id: Optional[str] = element(default=None)
    refunds: Optional[RefundsDTO] = element(default=None)

    @field_validator('create_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                return None
        return v

    @field_validator('amount', 'rev_max_amount', 'fee', mode='before')
    @classmethod
    def parse_amount(cls, v):
        if isinstance(v, str) and v.strip():
            try:
                return Decimal(v)
            except (ValueError, TypeError):
                return None
        return v

    @field_validator('ecode', 'edesc', 'auth_code', 'card_token', 'phone', 'desc_order',
                     'card_name', 'card_expdt', 'inv_exp_date', 'recur_freq', 'requr_exp',
                     'recur_ref', 'recur_int_ref', 'client_id', 'card_to_masked',
                     'cart_to_token', 'fee', 'merch_rn_id', mode='before')
    @classmethod
    def parse_empty_strings(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v


class AlatauRefundPaymentResultDTO(BaseXmlModel, tag='result'):
    code: int = element()
    description: str = element()
    operation: Optional[AlatauOperationDTO] = element(default=None)