import hashlib
import re
from typing import Optional

from app.infrastructure.app_config import app_config



class AlatauCreateResponseOrderDTO:
    def __init__(self):
        # Обязательные поля
        self.ORDER: Optional[str] = None
        self.AMOUNT: Optional[int] = None
        self.CURRENCY: Optional[str] = "KZT"
        self.MERCHANT: Optional[str] = app_config.merchant_id
        self.TERMINAL: Optional[str] = app_config.terminal_id
        self.DESC: Optional[str] = None

        # Необязательные поля
        self.DESC_ORDER: Optional[str] = None
        self.EMAIL: Optional[str] = None
        self.WTYPE: Optional[str] = "2"
        self.NAME: Optional[str] = None
        self.NONCE: Optional[str] = None
        self.CLIENT_ID: Optional[str] = None
        self.BACKREF: Optional[str] = app_config.ticketon_backref
        self.Ucaf_Flag: Optional[str] = None
        self.Ucaf_Authentication_Data: Optional[str] = None

        # Служебные
        self.P_SIGN: Optional[str] = None
        self.SIGNATURE_STRING: Optional[str] = None

    def generate_signature(self, shared_key: str) -> str:
        """
        Генерация P_SIGN по документации (sha512, shared_key + все поля через ;)
        """
        # Чистим переносы строк
        desc_clean = re.sub(r'[\n\r]', '', str(self.DESC or ''))
        desc_order_clean = re.sub(r'[\n\r]', '', str(self.DESC_ORDER or ''))

        # Только те поля, что реально участвуют в стенде
        signature_parts = [
            str(self.ORDER or ''),
            str(self.AMOUNT or ''),
            str(self.CURRENCY or ''),
            str(self.MERCHANT or ''),
            str(self.TERMINAL or ''),
            str(self.NONCE or ''),
            str(self.CLIENT_ID or ''),
            desc_clean,
            desc_order_clean,
            str(self.EMAIL or ''),
            str(self.BACKREF or ''),
            str(self.Ucaf_Flag or ''),
            str(self.Ucaf_Authentication_Data or ''),
            ''  # финальный ;
        ]

        signature_string = ';'.join(signature_parts)
        self.SIGNATURE_STRING = signature_string

        raw = shared_key + signature_string
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def set_signature(self, shared_key: str):
        """Заполняет self.P_SIGN"""
        self.P_SIGN = self.generate_signature(shared_key)
    
    def dict(self) -> dict:
        """Возвращает словарь всех атрибутов объекта"""
        return {
            'ORDER': self.ORDER,
            'AMOUNT': self.AMOUNT,
            'CURRENCY': self.CURRENCY,
            'MERCHANT': self.MERCHANT,
            'TERMINAL': self.TERMINAL,
            'DESC': self.DESC,
            'DESC_ORDER': self.DESC_ORDER,
            'EMAIL': self.EMAIL,
            'WTYPE': self.WTYPE,
            'NAME': self.NAME,
            'NONCE': self.NONCE,
            'CLIENT_ID': self.CLIENT_ID,
            'BACKREF': self.BACKREF,
            'Ucaf_Flag': self.Ucaf_Flag,
            'Ucaf_Authentication_Data': self.Ucaf_Authentication_Data,
            'P_SIGN': self.P_SIGN,
            'SIGNATURE_STRING': self.SIGNATURE_STRING,
        }

    class Config:
        from_attributes = True



