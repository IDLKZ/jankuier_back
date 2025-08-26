from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductCategoryEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ProductCategorySeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        categories = self.get_data()
        await self.load_seeders(
            ProductCategoryEntity, session, AppTableNames.ProductCategoryTableName, categories
        )

    def get_dev_data(self) -> list[ProductCategoryEntity]:
        return [
            ProductCategoryEntity(
                id=1,
                image_id=None,
                title_ru="Спортивная одежда",
                title_kk="Спорт киімдері",
                title_en="Sports Clothing",
                description_ru="Профессиональная спортивная одежда для тренировок и соревнований",
                description_kk="Жаттығулар мен жарыстарға арналған кәсіби спорт киімдері",
                description_en="Professional sports clothing for training and competitions",
                value=DbValueConstants.get_value("Спортивная одежда"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=2,
                image_id=None,
                title_ru="Спортивная обувь",
                title_kk="Спорт аяқ киімдері",
                title_en="Sports Footwear",
                description_ru="Специализированная обувь для различных видов спорта",
                description_kk="Әртүрлі спорт түрлеріне арналған мамандандырылған аяқ киім",
                description_en="Specialized footwear for various sports",
                value=DbValueConstants.get_value("Спортивная обувь"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=3,
                image_id=None,
                title_ru="Спортивное оборудование",
                title_kk="Спорт жабдықтары",
                title_en="Sports Equipment",
                description_ru="Инвентарь и оборудование для занятий спортом",
                description_kk="Спортпен айналысуға арналған инвентарь мен жабдықтар",
                description_en="Inventory and equipment for sports activities",
                value=DbValueConstants.get_value("Спортивное оборудование"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=4,
                image_id=None,
                title_ru="Аксессуары",
                title_kk="Аксессуарлар",
                title_en="Accessories",
                description_ru="Спортивные аксессуары и дополнительные товары",
                description_kk="Спорт аксессуарлары мен қосымша тауарлар",
                description_en="Sports accessories and additional items",
                value=DbValueConstants.get_value("Аксессуары"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=5,
                image_id=None,
                title_ru="Питание и добавки",
                title_kk="Тамақтану және қоспалар",
                title_en="Nutrition and Supplements",
                description_ru="Спортивное питание и биологически активные добавки",
                description_kk="Спорттық тамақтану және биологиялық белсенді қоспалар",
                description_en="Sports nutrition and dietary supplements",
                value=DbValueConstants.get_value("Питание и добавки"),
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ProductCategoryEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass