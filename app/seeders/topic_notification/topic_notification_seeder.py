from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import TopicNotificationEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class TopicNotificationSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        topics = self.get_data()
        await self.load_seeders(
            TopicNotificationEntity,
            session,
            AppTableNames.TopicNotificationTableName,
            topics,
        )

    def get_dev_data(self) -> list[TopicNotificationEntity]:
        return [
            TopicNotificationEntity(
                id=DbValueConstants.TopicNotificationAlertID,
                image_id=None,
                title_ru="Оповещение",
                title_kk="Хабарландыру",
                title_en="Alert",
                value=DbValueConstants.TopicNotificationAlertValue,
            ),
            TopicNotificationEntity(
                id=DbValueConstants.TopicNotificationShopID,
                image_id=None,
                title_ru="Магазин",
                title_kk="Дүкен",
                title_en="Shop",
                value=DbValueConstants.TopicNotificationShopValue,
            ),
            TopicNotificationEntity(
                id=DbValueConstants.TopicNotificationTicketsID,
                image_id=None,
                title_ru="Билеты",
                title_kk="Билеттер",
                title_en="Tickets",
                value=DbValueConstants.TopicNotificationTicketsValue,
            ),
            TopicNotificationEntity(
                id=DbValueConstants.TopicNotificationFieldsID,
                image_id=None,
                title_ru="Поля",
                title_kk="Алаңдар",
                title_en="Fields",
                value=DbValueConstants.TopicNotificationFieldsValue,
            ),
            TopicNotificationEntity(
                id=DbValueConstants.TopicNotificationPaymentID,
                image_id=None,
                title_ru="Оплата",
                title_kk="Төлем",
                title_en="Payment",
                value=DbValueConstants.TopicNotificationPaymentValue,
            ),
        ]

    def get_prod_data(self) -> list[TopicNotificationEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass
