from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.booking_field_party_status_entity import BookingFieldPartyStatusEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class BookingFieldPartyStatusSeeder(BaseSeeder):
    """
    Сидер для статусов бронирования площадок.
    Создает 5 статусов: создана (ожидает оплаты), оплачена, отменена,
    отменена (ожидает возврата), отменена (возвращена).
    """

    async def seed(self, session: AsyncSession) -> None:
        entities = self.get_data()
        await self.load_seeders(
            BookingFieldPartyStatusEntity,
            session,
            AppTableNames.BookingFieldPartyStatusTableName,
            entities,
        )

    def get_dev_data(self) -> list[BookingFieldPartyStatusEntity]:
        return [
            BookingFieldPartyStatusEntity(
                id=DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentID,
                previous_id=None,
                next_id=DbValueConstants.BookingFieldPartyStatusPaidID,
                value=DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentValue,
                title_ru="Бронь создана, ожидает оплаты",
                title_kk="Брондау жасалды, төлемді күтуде",
                title_en="Booking created, awaiting payment",
                is_first=True,
                is_active=True,
                is_last=False,
                previous_allowed_values=None,
                next_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusPaidValue,
                    DbValueConstants.BookingFieldPartyStatusCancelledValue,
                ],
            ),
            BookingFieldPartyStatusEntity(
                id=DbValueConstants.BookingFieldPartyStatusPaidID,
                previous_id=DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentID,
                next_id=DbValueConstants.BookingFieldPartyStatusCancelledID,
                value=DbValueConstants.BookingFieldPartyStatusPaidValue,
                title_ru="Бронь оплачена",
                title_kk="Брондау төленді",
                title_en="Booking paid",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentValue,
                ],
                next_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCancelledValue,
                ],
            ),
            BookingFieldPartyStatusEntity(
                id=DbValueConstants.BookingFieldPartyStatusCancelledID,
                previous_id=DbValueConstants.BookingFieldPartyStatusPaidID,
                next_id=DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundID,
                value=DbValueConstants.BookingFieldPartyStatusCancelledValue,
                title_ru="Бронь отменена",
                title_kk="Брондау жойылды",
                title_en="Booking cancelled",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCreatedAwaitingPaymentValue,
                    DbValueConstants.BookingFieldPartyStatusPaidValue,
                ],
                next_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundValue,
                ],
            ),
            BookingFieldPartyStatusEntity(
                id=DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundID,
                previous_id=DbValueConstants.BookingFieldPartyStatusCancelledID,
                next_id=DbValueConstants.BookingFieldPartyStatusCancelledRefundedID,
                value=DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundValue,
                title_ru="Бронь отменена, ожидает возврата средств",
                title_kk="Брондау жойылды, қаражатты қайтару күтілуде",
                title_en="Booking cancelled, awaiting refund",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCancelledValue,
                ],
                next_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCancelledRefundedValue,
                ],
            ),
            BookingFieldPartyStatusEntity(
                id=DbValueConstants.BookingFieldPartyStatusCancelledRefundedID,
                previous_id=DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundID,
                next_id=None,
                value=DbValueConstants.BookingFieldPartyStatusCancelledRefundedValue,
                title_ru="Бронь отменена, средства возвращены",
                title_kk="Брондау жойылды, қаражат қайтарылды",
                title_en="Booking cancelled, refunded",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[
                    DbValueConstants.BookingFieldPartyStatusCancelledAwaitingRefundValue,
                ],
                next_allowed_values=None,
            ),
        ]

    def get_prod_data(self) -> list[BookingFieldPartyStatusEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> list[dict]:
        return []

    def get_prod_updated_data(self) -> list[dict]:
        return []