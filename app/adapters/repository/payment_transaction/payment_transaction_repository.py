import random
import string
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.repository.base_repository import BaseRepository
from app.entities import PaymentTransactionEntity


class PaymentTransactionRepository(BaseRepository[PaymentTransactionEntity]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(PaymentTransactionEntity, db)

    def default_relationships(self) -> list[Any]:
        return [
            selectinload(self.model.user),
            selectinload(self.model.status)
        ]

    async def generate_unique_order(self,min_len: int = 6, max_len: int = 22) -> str:
        """
        Генерирует уникальный order (строка из цифр длиной 6–22),
        проверяет, что в БД такого нет.
        """
        while True:
            length = random.randint(min_len, max_len)
            new_order = ''.join(random.choices(string.digits, k=length))

            exist = await self.get_first_with_filters(filters=[self.model.order == new_order])
            if not exist:
                return new_order



    async def generate_unique_noncense(self,min_len: int = 6, max_len: int = 64) -> str:
        """
        Генерирует уникальный new_nonce (строка из цифр длиной 6–64),
        проверяет, что в БД такого нет.
        """
        while True:
            length = random.randint(min_len, max_len)
            new_nonce = ''.join(random.choices(string.digits, k=length))

            exist = await self.get_first_with_filters(filters=[self.model.nonce == new_nonce])
            if not exist:
                return new_nonce