import hashlib
import re
import urllib.parse
from pydantic import BaseModel
from typing import Optional

from app.adapters.dto.payment_transaction.payment_transaction_dto import PaymentTransactionWithRelationsRDTO
from app.adapters.dto.ticketon_order.ticketon_order_dto import TicketonOrderWithRelationsRDTO, TicketonOrderRDTO
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
    """
    DTO для результата платежа при GET-редиректе (BACKREF URL).

    Порядок полей для подписи согласно документации Alatau:
    order, mpi_order, rrn, res_code, amount, currency, res_desc
    """

    redirect: Optional[str] = None                 # Флаг редиректа (не участвует в подписи)
    order: Optional[str] = None                    # Номер заказа
    mpi_order: Optional[str] = None                # Номер заказа в MPI
    rrn: Optional[str] = None                      # Retrieval Reference Number
    int_ref: Optional[str] = None                  # Internal Reference (не участвует в подписи)
    res_code: Optional[str] = None                 # Код результата (0=успех)
    amount: Optional[str] = None                   # Сумма
    currency: Optional[str] = None                 # Валюта (например KZT, EUR)
    res_desc: Optional[str] = None                 # Текстовое описание результата
    sign: Optional[str] = None                     # Подпись

    def generate_signature(self, shared_key: str) -> str:
        """
        Формирует подпись по правилам Alatau GET BACKREF.

        Алгоритм согласно документации:
        1. Собираем поля в порядке: order, mpi_order, rrn, res_code, amount, currency, res_desc
        2. Разделяем их символом ";"
        3. В res_desc убираем переносы строк (\n\r)
        4. Добавляем shared_key в начало строки
        5. Вычисляем SHA512 хэш
        """
        # Декодируем и очищаем res_desc от переносов строк
        desc_decoded = urllib.parse.unquote_plus(self.res_desc or '')
        res_desc_clean = re.sub(r'[\n\r]', '', desc_decoded)

        # Собираем поля в правильном порядке согласно документации
        signature_parts = [
            str(self.order or ''),
            str(self.mpi_order or ''),
            str(self.rrn or ''),
            str(self.res_code or ''),
            str(self.amount or ''),
            str(self.currency or ''),
            res_desc_clean + ';'  # завершающий ";" согласно PHP примеру
        ]

        # Соединяем через ";"
        signature_string = ';'.join(signature_parts)

        # Добавляем shared_key в начало и вычисляем SHA512
        raw = shared_key + signature_string
        print("Строка для подписи",raw)
        return hashlib.sha512(raw.encode("utf-8")).hexdigest()

    def verify_signature(self, shared_key: str) -> bool:
        """Проверяет совпадение подписи"""
        print("Подпись сгенерированная по документации",self.generate_signature(shared_key))
        print("Подпись отправленная от банка",self.sign)
        return self.generate_signature(shared_key) == self.sign


class AlatauBackrefResponseDTO(BaseModel):
    ticketon_order:TicketonOrderWithRelationsRDTO|None = None
    payment_transaction:PaymentTransactionWithRelationsRDTO|None = None
    status:DTOConstant.StandardBooleanFalseField(description="Код результата (0=успех)") = False
    message:DTOConstant.StandardNullableTextField(description="Доп. описание")

    class Config:
        from_attributes = True