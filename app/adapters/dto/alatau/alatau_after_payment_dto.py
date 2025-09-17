import hashlib
import re
import urllib.parse
from pydantic import BaseModel
from typing import Optional

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO
from app.entities import TicketonOrderEntity
from app.shared.dto_constants import DTOConstant


class AlatauBackrefPostDTO(BaseModel):
    """
    DTO для результата платежа (redirect callback BACKREF).
    Используется при возврате клиента на сайт коммерсанта.
    """

    order: str               # ID заказа на стороне мерчанта
    mpi_order: str           # ID транзакции в MPI
    amount: str            # Сумма платежа
    currency: str            # Валюта (например EUR, KZT)
    res_code: str            # Код результата (0 = успех)
    rc: str                  # Response Code (например "00")
    rrn: Optional[str] = None  # Retrieval Reference Number (уникальный ID в банке)
    sign: str                # Подпись банка

    def generate_signature(self, shared_key: str) -> str:
        """
        Генерация подписи для проверки (sha512, shared_key + все поля через ;)
        """
        signature_parts = [
            str(self.order or ''),
            str(self.mpi_order or ''),
            str(self.amount or ''),
            str(self.currency or ''),
            str(self.res_code or ''),
            str(self.rc or ''),
            str(self.rrn or ''),
            ''  # завершающий ";"
        ]
        signature_string = ';'.join(signature_parts)
        raw = shared_key + signature_string
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def verify_signature(self, shared_key: str) -> bool:
        """Сравнивает подпись от банка с рассчитанной"""
        expected = self.generate_signature(shared_key)
        return expected == self.sign



class AlatauBackrefGetDTO(BaseModel):
    """DTO для результата платежа при GET-редиректе (BACKREF URL)"""

    order: str                    # Номер заказа
    mpi_order: str                # Номер заказа в MPI
    res_code: str                 # Код результата (0=успех)
    amount: str                 # Сумма
    currency: str                 # Валюта
    res_desc: Optional[str] = None  # Текстовое описание результата
    rrn: Optional[str] = None      # Доп. описание
    sign: str                     # Подпись

    def generate_signature(self, shared_key: str) -> str:
        """Формирует подпись по правилам Alatau GET BACKREF"""
        desc_decoded = urllib.parse.unquote_plus(self.res_desc or '')
        res_desc_clean = re.sub(r'[\n\r]', '', desc_decoded)

        signature_parts = [
            str(self.order or ''),
            str(self.mpi_order or ''),
            str(self.rrn or ''),
            str(self.res_code or ''),
            str(self.amount or ''),
            str(self.currency or ''),
            res_desc_clean,
            ''
        ]

        signature_string = ';'.join(signature_parts)
        raw = shared_key + signature_string

        print("🧪 RAW:", repr(raw))
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def verify_signature(self, shared_key: str) -> bool:
        """Проверяет совпадение подписи"""
        print(self.generate_signature(shared_key))
        return self.generate_signature(shared_key) == self.sign


class AlatauBackrefResponseDTO(BaseModel):
    ticketon_order:TicketonOrderWithRelationsRDTO|None = None
    payment_transaction:PaymentTransactionWithRelationsRDTO|None = None
    status:DTOConstant.StandardBooleanFalseField(description="Код результата (0=успех)") = False
    message:DTOConstant.StandardNullableTextField(description="Доп. описание")

    class Config:
        from_attributes = True