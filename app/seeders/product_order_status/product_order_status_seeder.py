from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductOrderStatusEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ProductOrderStatusSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        statuses = self.get_data()
        await self.load_seeders(ProductOrderStatusEntity, session, AppTableNames.ProductOrderStatusTableName, statuses)

    def get_dev_data(self) -> list[ProductOrderStatusEntity]:
        return [
            ProductOrderStatusEntity(
                id=DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,
                previous_id=None,
                next_id=DbValueConstants.ProductOrderStatusPaidID,
                title_ru="Заказ создан, ожидает оплаты",
                title_kk="Тапсырыс жасалды, төлемді күтуде",
                title_en="Order created, awaiting payment",
                is_first=True,
                is_active=True,
                is_last=False,
                previous_allowed_values=None,
                next_allowed_values=[DbValueConstants.ProductOrderStatusPaidValue, DbValueConstants.ProductOrderStatusCancelledValue],
            ),
            ProductOrderStatusEntity(
                id=DbValueConstants.ProductOrderStatusPaidID,
                previous_id=DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,
                next_id=None,
                title_ru="Заказ оплачен",
                title_kk="Тапсырыс төленді",
                title_en="Order paid",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentValue],
                next_allowed_values=[DbValueConstants.ProductOrderStatusCancelledAwaitingRefundValue],
            ),
            ProductOrderStatusEntity(
                id=DbValueConstants.ProductOrderStatusCancelledID,
                previous_id=DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentID,
                next_id=None,
                title_ru="Заказ отменен",
                title_kk="Тапсырыс жойылды",
                title_en="Order cancelled",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderStatusCreatedAwaitingPaymentValue],
                next_allowed_values=None,
            ),
            ProductOrderStatusEntity(
                id=DbValueConstants.ProductOrderStatusCancelledAwaitingRefundID,
                previous_id=DbValueConstants.ProductOrderStatusPaidID,
                next_id=DbValueConstants.ProductOrderStatusCancelledRefundedID,
                title_ru="Заказ отменен, ожидает возврата средства",
                title_kk="Тапсырыс жойылды, ақшаның қайтарылуын күтуде",
                title_en="Order cancelled, awaiting refund",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[DbValueConstants.ProductOrderStatusPaidValue],
                next_allowed_values=[DbValueConstants.ProductOrderStatusCancelledRefundedValue],
            ),
            ProductOrderStatusEntity(
                id=DbValueConstants.ProductOrderStatusCancelledRefundedID,
                previous_id=DbValueConstants.ProductOrderStatusCancelledAwaitingRefundID,
                next_id=None,
                title_ru="Заказ отменен, средства возвращены",
                title_kk="Тапсырыс жойылды, ақша қайтарылды",
                title_en="Order cancelled, refunded",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderStatusCancelledAwaitingRefundValue],
                next_allowed_values=None,
            ),
        ]

    def get_prod_data(self) -> list[ProductOrderStatusEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass