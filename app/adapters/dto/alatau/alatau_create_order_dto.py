import hashlib
import re
from decimal import Decimal, ROUND_DOWN
from typing import Optional

from pydantic import BaseModel, field_validator, field_serializer
from app.infrastructure.app_config import app_config


class AlatauCreateResponseOrderDTO(BaseModel):
    # Обязательные поля
    ORDER: Optional[str] = None
    AMOUNT: Optional[Decimal|str|int] = None
    CURRENCY: Optional[str] = "KZT"
    MERCHANT: Optional[str] = app_config.merchant_id
    TERMINAL: Optional[str] = app_config.terminal_id
    DESC: Optional[str] = None

    # Необязательные поля
    DESC_ORDER: Optional[str] = None
    EMAIL: Optional[str] = None
    WTYPE: Optional[str] = "2"
    NAME: Optional[str] = None
    NONCE: Optional[str] = None
    CLIENT_ID: Optional[int|str] = None
    BACKREF: Optional[str] = app_config.ticketon_backref
    Ucaf_Flag: Optional[str] = None
    Ucaf_Authentication_Data: Optional[str] = None

    # Служебные
    P_SIGN: Optional[str] = None
    SIGNATURE_STRING: Optional[str] = None

    class Config:
        from_attributes = True

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
            self._format_amount(),
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

        # сохраняем "чистую" строку для отладки
        self.SIGNATURE_STRING = signature_string

        # подписываем только с ключом
        raw = shared_key + signature_string
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def set_signature(self, shared_key: str):
        """Заполняет self.P_SIGN"""
        self.P_SIGN = self.generate_signature(shared_key)

    def _format_amount(self) -> str:
        """
        Форматирует amount согласно правилам:
        - 100 -> 100.0
        - 100.0 -> 100.0
        - 100.05 -> 100.05
        - 100.055 -> 100.05 (округление вниз до 2 знаков)
        """
        if self.AMOUNT is None:
            return ''

        # Приводим к Decimal для точности
        amount = Decimal(str(self.AMOUNT))

        # Округляем вниз до 2 знаков после запятой
        rounded_amount = amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        # Форматируем с всегда 1 знаком после запятой минимум
        formatted = format(rounded_amount, '.2f')

        # Если заканчивается на .00, меняем на .0
        if formatted.endswith('.00'):
            return formatted[:-1]  # убираем последний 0
        # Если заканчивается на 0 (например 100.50), убираем последний 0
        elif formatted.endswith('0') and '.' in formatted:
            return formatted[:-1]

        return formatted

    def _format_amount_from_decimal(self, amount: Decimal) -> str:
        """
        Форматирует Decimal amount согласно правилам:
        - 100 -> 100.0
        - 100.0 -> 100.0
        - 100.05 -> 100.05
        - 100.055 -> 100.05 (округление вниз до 2 знаков)
        """
        if amount is None:
            return ''

        # Округляем вниз до 2 знаков после запятой
        rounded_amount = amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        # Форматируем с всегда 2 знаками после запятой
        formatted = format(rounded_amount, '.2f')

        # Если заканчивается на .00, меняем на .0
        if formatted.endswith('.00'):
            return formatted[:-1]  # убираем последний 0
        # Если заканчивается на 0 (например 100.50), убираем последний 0
        elif formatted.endswith('0') and '.' in formatted:
            return formatted[:-1]

        return formatted

    # --- сеттер через валидатор Pydantic
    @field_validator("AMOUNT", mode="before")
    @classmethod
    def _set_amount(cls, v):
        """Валидатор для поля AMOUNT - округляет до 2 знаков вниз"""
        if v is None:
            return None
        # приводим к Decimal
        amount = Decimal(str(v))
        # режем до двух знаков вниз
        return amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

    # --- сериализация для JSON (тот же формат, что в подписи)
    @field_serializer("AMOUNT")
    def _serialize_amount(self, v: Optional[Decimal|int|str], _info):
        """Сериализатор для поля AMOUNT - применяет правила форматирования"""
        if v is None:
            return None
        # Конвертируем в Decimal если еще не Decimal
        if not isinstance(v, Decimal):
            v = Decimal(str(v))
        return self._format_amount_from_decimal(v)


