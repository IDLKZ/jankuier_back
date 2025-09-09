from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import TicketonOrderStatusEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class TicketonOrderStatusSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        statuses = self.get_data()
        await self.load_seeders(
            TicketonOrderStatusEntity, 
            session, 
            AppTableNames.TicketonOrderStatusTableName, 
            statuses
        )

    def get_dev_data(self) -> list[TicketonOrderStatusEntity]:
        return [
            # 1. Бронь создана ожидает оплаты
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusBookingCreatedID,
                previous_id=None,
                next_id=DbValueConstants.TicketonOrderStatusPaidConfirmedID,
                title_ru="Бронь создана, ожидает оплаты",
                title_kk="Бронь жасалды, төлемді күтуде",
                title_en="Booking created, awaiting payment",
                is_first=True,
                is_active=True,
                is_last=False,
            ),
            # 2. Оплачено и подтверждено
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusPaidConfirmedID,
                previous_id=DbValueConstants.TicketonOrderStatusBookingCreatedID,
                next_id=None,  # Может переходить к отмене
                title_ru="Оплачено и подтверждено",
                title_kk="Төленді және расталды",
                title_en="Paid and confirmed",
                is_first=False,
                is_active=True,
                is_last=True,
            ),
            # 3. Оплачено, ожидает подтверждения
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusPaidAwaitingConfirmationID,
                previous_id=DbValueConstants.TicketonOrderStatusBookingCreatedID,
                next_id=DbValueConstants.TicketonOrderStatusPaidConfirmedID,
                title_ru="Оплачено, ожидает подтверждения",
                title_kk="Төленді, растауды күтуде",
                title_en="Paid, awaiting confirmation",
                is_first=False,
                is_active=True,
                is_last=False,
            ),
            # 4. Отменено
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusCancelledID,
                previous_id=None,  # Может быть отменено с любого статуса
                next_id=DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                title_ru="Отменено",
                title_kk="Болдырылмады",
                title_en="Cancelled",
                is_first=False,
                is_active=False,
                is_last=False,
            ),
            # 5. Отменено, ожидание возврата оплаты
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                previous_id=DbValueConstants.TicketonOrderStatusCancelledID,
                next_id=DbValueConstants.TicketonOrderStatusCancelledRefundedID,
                title_ru="Отменено, ожидание возврата оплаты",
                title_kk="Болдырылмады, төлемді қайтаруды күтуде",
                title_en="Cancelled, awaiting refund",
                is_first=False,
                is_active=False,
                is_last=False,
            ),
            # 6. Отменено, оплата возвращена
            TicketonOrderStatusEntity(
                id=DbValueConstants.TicketonOrderStatusCancelledRefundedID,
                previous_id=DbValueConstants.TicketonOrderStatusCancelledAwaitingRefundID,
                next_id=None,
                title_ru="Отменено, оплата возвращена",
                title_kk="Болдырылмады, төлем қайтарылды",
                title_en="Cancelled, refunded",
                is_first=False,
                is_active=False,
                is_last=True,
            ),
        ]

    def get_prod_data(self) -> list[TicketonOrderStatusEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> list[dict]:
        return []

    def get_prod_updated_data(self) -> list[dict]:
        return []