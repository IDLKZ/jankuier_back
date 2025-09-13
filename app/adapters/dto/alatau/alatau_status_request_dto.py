import hashlib
from typing import Optional

from pydantic import BaseModel

from app.infrastructure.app_config import app_config


class AlatauStatusRequestDTO(BaseModel):
    """
    DTO для запроса статуса платежа в системе Alatau.

    Поля для запроса статуса:
    - ORDER: str - номер заказа (обязательное)
    - MERCHANT: str - идентификатор мерчанта (из конфигурации, обязательное)
    - GETSTATUS: int - флаг запроса статуса, всегда = 1 (обязательное)
    - LANGUAGE: Optional[str] - язык (опционально)
    - P_SIGN: str - подпись для верификации
    """

    # Обязательные поля для запроса статуса
    ORDER: str = ""
    MERCHANT: str = app_config.merchant_id
    GETSTATUS: int = 1

    # Необязательные поля
    LANGUAGE: Optional[str] = "ru"

    # Служебные поля
    P_SIGN: str = ""
    SIGNATURE_STRING: str = ""

    def generate_signature(self, shared_key: str) -> str:
        """
        Генерация P_SIGN для запроса статуса по формуле:
        hash("sha512", SHARED_KEY + ORDER + ";" + MERCHANT)

        Args:
            shared_key: секретный ключ для подписи

        Returns:
            str: SHA512 хеш подписи
        """
        # Формируем строку для подписи согласно формуле
        # C_SHARED_KEY.$_POST["ORDER"].";".$_POST["MERCHANT"]
        signature_string = f"{self.ORDER};{self.MERCHANT}"
        self.SIGNATURE_STRING = signature_string

        # Формируем итоговую строку: shared_key + signature_string
        raw = shared_key + signature_string
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def set_signature(self, shared_key: str):
        """
        Заполняет поле P_SIGN подписью

        Args:
            shared_key: секретный ключ для подписи
        """
        self.P_SIGN = self.generate_signature(shared_key)

    def dict(self) -> dict:
        """
        Возвращает словарь всех атрибутов объекта для отправки в API
        (для обратной совместимости)

        Returns:
            dict: словарь с полями DTO
        """
        return self.model_dump()

    def model_dump(self) -> dict:
        """
        Возвращает словарь всех атрибутов объекта для отправки в API

        Returns:
            dict: словарь с полями DTO
        """
        return super().model_dump()

    def to_form_data(self) -> dict:
        """
        Возвращает словарь только с обязательными полями для отправки в форме
        (исключает служебные поля SIGNATURE_STRING)

        Returns:
            dict: словарь с полями для HTTP формы
        """
        form_data = {
            'ORDER': self.ORDER,
            'MERCHANT': self.MERCHANT,
            'GETSTATUS': str(self.GETSTATUS),
            'P_SIGN': self.P_SIGN,
        }

        if self.LANGUAGE is not None:
            form_data['LANGUAGE'] = self.LANGUAGE

        return form_data

    def validate(self) -> list[str]:
        """
        Валидация обязательных полей

        Returns:
            list[str]: список ошибок валидации
        """
        errors = []

        if not self.ORDER:
            errors.append("ORDER is required")
        if not self.MERCHANT:
            errors.append("MERCHANT is required")
        if self.GETSTATUS != 1:
            errors.append("GETSTATUS must be 1")
        if not self.P_SIGN:
            errors.append("P_SIGN is required (call set_signature first)")

        return errors

    def __str__(self) -> str:
        """Строковое представление объекта"""
        return f"AlatauStatusResponseDTO(ORDER={self.ORDER}, MERCHANT={self.MERCHANT}, GETSTATUS={self.GETSTATUS})"

    class Config:
        from_attributes = True