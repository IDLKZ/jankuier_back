from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import PaymentTransactionStatusEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class PaymentTransactionStatusSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        statuses = self.get_data()
        await self.load_seeders(
            PaymentTransactionStatusEntity, 
            session, 
            AppTableNames.PaymentTransactionStatusTableName, 
            statuses
        )

    def get_dev_data(self) -> list[PaymentTransactionStatusEntity]:
        return [
            # 1. Ожидает оплаты
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                previous_id=None,
                next_id=DbValueConstants.PaymentTransactionStatusPaidID,
                title_ru="Ожидает оплаты",
                title_kk="Төлемді күтуде",
                title_en="Awaiting payment",
                is_first=True,
                is_active=True,
                is_last=False,
            ),
            # 2. Оплачено
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusPaidID,
                previous_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                next_id=None,  # Может переходить к отмене или возврату
                title_ru="Оплачено",
                title_kk="Төленді",
                title_en="Paid",
                is_first=False,
                is_active=True,
                is_last=True,
            ),
            # 3. Отменено
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusCancelledID,
                previous_id=None,  # Может быть отменено с любого статуса
                next_id=None,
                title_ru="Отменено",
                title_kk="Болдырылмады",
                title_en="Cancelled",
                is_first=False,
                is_active=False,
                is_last=True,
            ),
            # 4. Провалено
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusFailedID,
                previous_id=DbValueConstants.PaymentTransactionStatusAwaitingPaymentID,
                next_id=None,
                title_ru="Провалено",
                title_kk="Сәтсіз",
                title_en="Failed",
                is_first=False,
                is_active=False,
                is_last=True,
            ),
            # 5. Ожидает возврата средств
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusAwaitingRefundID,
                previous_id=DbValueConstants.PaymentTransactionStatusPaidID,
                next_id=DbValueConstants.PaymentTransactionStatusRefundedID,
                title_ru="Ожидает возврата средств",
                title_kk="Қаражатты қайтаруды күтуде",
                title_en="Awaiting refund",
                is_first=False,
                is_active=True,
                is_last=False,
            ),
            # 6. Средства возвращены
            PaymentTransactionStatusEntity(
                id=DbValueConstants.PaymentTransactionStatusRefundedID,
                previous_id=DbValueConstants.PaymentTransactionStatusAwaitingRefundID,
                next_id=None,
                title_ru="Средства возвращены",
                title_kk="Қаражат қайтарылды",
                title_en="Refunded",
                is_first=False,
                is_active=True,
                is_last=True,
            ),
        ]

    def get_prod_data(self) -> list[PaymentTransactionStatusEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> list[dict]:
        return []

    def get_prod_updated_data(self) -> list[dict]:
        return []