from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductOrderItemStatusEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ProductOrderItemStatusSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        statuses = self.get_data()
        await self.load_seeders(ProductOrderItemStatusEntity, session, AppTableNames.ProductOrderItemStatusTableName, statuses)

    def get_dev_data(self) -> list[ProductOrderItemStatusEntity]:
        return [
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,
                previous_id=None,
                next_id=DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID,
                title_ru="Заказ создан, ожидает оплаты",
                title_kk="Тапсырыс жасалды, төлемді күтуде",
                title_en="Order created, awaiting payment",
                is_first=True,
                is_active=True,
                is_last=False,
                previous_allowed_values=None,
                next_allowed_values=[DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationValue, DbValueConstants.ProductOrderItemStatusCancelledValue],
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID,
                previous_id=DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,
                next_id=DbValueConstants.ProductOrderItemStatusInDeliveryID,
                title_ru="Заказ оплачен, ожидает подтверждения",
                title_kk="Тапсырыс төленді, растауды күтуде",
                title_en="Order paid, awaiting confirmation",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentValue],
                next_allowed_values=[DbValueConstants.ProductOrderItemStatusInDeliveryValue, DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundValue],
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusInDeliveryID,
                previous_id=DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID,
                next_id=DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID,
                title_ru="Заказ доставляется",
                title_kk="Тапсырыс жеткізілуде",
                title_en="Order in delivery",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationValue],
                next_allowed_values=[DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationValue, DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundValue],
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID,
                previous_id=DbValueConstants.ProductOrderItemStatusInDeliveryID,
                next_id=DbValueConstants.ProductOrderItemStatusSuccessfullyReceivedID,
                title_ru="Заказ ожидает подтверждения доставки",
                title_kk="Тапсырыс жеткізудің растауын күтуде",
                title_en="Order awaiting delivery confirmation",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusInDeliveryValue],
                next_allowed_values=[DbValueConstants.ProductOrderItemStatusSuccessfullyReceivedValue, DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundValue],
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusSuccessfullyReceivedID,
                previous_id=DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID,
                next_id=None,
                title_ru="Заказ успешно получен",
                title_kk="Тапсырыс сәтті алынды",
                title_en="Order successfully received",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationValue],
                next_allowed_values=None,
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusCancelledID,
                previous_id=DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,
                next_id=None,
                title_ru="Заказ отменен",
                title_kk="Тапсырыс жойылды",
                title_en="Order cancelled",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentValue],
                next_allowed_values=None,
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID,
                previous_id=None,
                next_id=DbValueConstants.ProductOrderItemStatusCancelledRefundedID,
                title_ru="Заказ отменен, ожидает возврата средства",
                title_kk="Тапсырыс жойылды, ақшаның қайтарылуын күтуде",
                title_en="Order cancelled, awaiting refund",
                is_first=False,
                is_active=True,
                is_last=False,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusCancelledValue, DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationValue, DbValueConstants.ProductOrderItemStatusInDeliveryValue, DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationValue],
                next_allowed_values=[DbValueConstants.ProductOrderItemStatusCancelledRefundedValue],
            ),
            ProductOrderItemStatusEntity(
                id=DbValueConstants.ProductOrderItemStatusCancelledRefundedID,
                previous_id=DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID,
                next_id=None,
                title_ru="Заказ отменен, средства возвращены",
                title_kk="Тапсырыс жойылды, ақша қайтарылды",
                title_en="Order cancelled, refunded",
                is_first=False,
                is_active=True,
                is_last=True,
                previous_allowed_values=[DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundValue],
                next_allowed_values=None,
            ),
        ]

    def get_prod_data(self) -> list[ProductOrderItemStatusEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass