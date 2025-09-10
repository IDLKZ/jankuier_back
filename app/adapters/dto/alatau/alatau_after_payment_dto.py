import hashlib
import re

from pydantic import BaseModel
from typing import Optional

class AlatauBackrefPostDTO(BaseModel):
    """
    DTO для результата платежа (redirect callback BACKREF).
    Используется при возврате клиента на сайт коммерсанта.
    """

    order: str               # ID заказа на стороне мерчанта
    mpi_order: str           # ID транзакции в MPI
    amount: float            # Сумма платежа
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
    amount: float                 # Сумма
    currency: str                 # Валюта
    res_desc: Optional[str] = None  # Текстовое описание результата
    desc: Optional[str] = None      # Доп. описание
    sign: str                     # Подпись

    def generate_signature(self, shared_key: str) -> str:
        """Формирует подпись по правилам Alatau GET BACKREF"""
        res_desc_clean = re.sub(r'[\n\r]', '', str(self.res_desc or ''))

        signature_parts = [
            str(self.order or ''),
            str(self.mpi_order or ''),
            str(self.rrn or ''),
            str(self.res_code or ''),
            str(self.amount or ''),
            str(self.currency or ''),
            res_desc_clean,
            ''  # финальный ";"
        ]
        signature_string = ';'.join(signature_parts)
        raw = shared_key + signature_string
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def verify_signature(self, shared_key: str) -> bool:
        """Проверяет совпадение подписи"""
        return self.generate_signature(shared_key) == self.sign