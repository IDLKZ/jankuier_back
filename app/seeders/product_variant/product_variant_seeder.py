from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductVariantEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ProductVariantSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        product_variants = self.get_data()
        await self.load_seeders(
            ProductVariantEntity, session, AppTableNames.ProductVariantTableName, product_variants
        )

    def get_dev_data(self) -> list[ProductVariantEntity]:
        return [
            # Варианты для Футболки Nike Pro (product_id=1)
            ProductVariantEntity(
                id=1,
                product_id=1,
                image_id=None,
                city_id=None,
                title_ru="Футболка Nike Pro - Черная S",
                title_kk="Nike Pro футболкасы - Қара S",
                title_en="Nike Pro T-Shirt - Black S",
                value=DbValueConstants.get_value("Футболка Nike Pro - Черная S"),
                sku="NIKE-PRO-BLK-S",
                price_delta=Decimal("0.00"),
                stock=25,
                is_active=True,
                is_default=True,
            ),
            ProductVariantEntity(
                id=2,
                product_id=1,
                image_id=None,
                city_id=None,
                title_ru="Футболка Nike Pro - Черная M",
                title_kk="Nike Pro футболкасы - Қара M",
                title_en="Nike Pro T-Shirt - Black M",
                value=DbValueConstants.get_value("Футболка Nike Pro - Черная M"),
                sku="NIKE-PRO-BLK-M",
                price_delta=Decimal("0.00"),
                stock=30,
                is_active=True,
                is_default=False,
            ),
            ProductVariantEntity(
                id=3,
                product_id=1,
                image_id=None,
                city_id=None,
                title_ru="Футболка Nike Pro - Белая S",
                title_kk="Nike Pro футболкасы - Ақ S",
                title_en="Nike Pro T-Shirt - White S",
                value=DbValueConstants.get_value("Футболка Nike Pro - Белая S"),
                sku="NIKE-PRO-WHT-S",
                price_delta=Decimal("0.00"),
                stock=20,
                is_active=True,
                is_default=False,
            ),
            # Варианты для Спортивного костюма Adidas (product_id=2)
            ProductVariantEntity(
                id=4,
                product_id=2,
                image_id=None,
                city_id=None,
                title_ru="Спортивный костюм Adidas - Синий M",
                title_kk="Adidas спорт костюмы - Көк M",
                title_en="Adidas Sports Suit - Blue M",
                value=DbValueConstants.get_value("Спортивный костюм Adidas - Синий M"),
                sku="ADIDAS-SUIT-BLU-M",
                price_delta=Decimal("0.00"),
                stock=15,
                is_active=True,
                is_default=True,
            ),
            ProductVariantEntity(
                id=5,
                product_id=2,
                image_id=None,
                city_id=None,
                title_ru="Спортивный костюм Adidas - Синий L",
                title_kk="Adidas спорт костюмы - Көк L",
                title_en="Adidas Sports Suit - Blue L",
                value=DbValueConstants.get_value("Спортивный костюм Adidas - Синий L"),
                sku="ADIDAS-SUIT-BLU-L",
                price_delta=Decimal("500.00"),
                stock=12,
                is_active=True,
                is_default=False,
            ),
            # Варианты для кроссовок Nike Air Max (product_id=3)
            ProductVariantEntity(
                id=6,
                product_id=3,
                image_id=None,
                city_id=None,
                title_ru="Кроссовки Nike Air Max - Размер 42",
                title_kk="Nike Air Max кроссовкалары - 42 өлшем",
                title_en="Nike Air Max Sneakers - Size 42",
                value=DbValueConstants.get_value("Кроссовки Nike Air Max - Размер 42"),
                sku="NIKE-AIRMAX-42",
                price_delta=Decimal("0.00"),
                stock=8,
                is_active=True,
                is_default=True,
            ),
            ProductVariantEntity(
                id=7,
                product_id=3,
                image_id=None,
                city_id=None,
                title_ru="Кроссовки Nike Air Max - Размер 43",
                title_kk="Nike Air Max кроссовкалары - 43 өлшем",
                title_en="Nike Air Max Sneakers - Size 43",
                value=DbValueConstants.get_value("Кроссовки Nike Air Max - Размер 43"),
                sku="NIKE-AIRMAX-43",
                price_delta=Decimal("0.00"),
                stock=10,
                is_active=True,
                is_default=False,
            ),
            ProductVariantEntity(
                id=8,
                product_id=3,
                image_id=None,
                city_id=None,
                title_ru="Кроссовки Nike Air Max - Размер 44",
                title_kk="Nike Air Max кроссовкалары - 44 өлшем",
                title_en="Nike Air Max Sneakers - Size 44",
                value=DbValueConstants.get_value("Кроссовки Nike Air Max - Размер 44"),
                sku="NIKE-AIRMAX-44",
                price_delta=Decimal("0.00"),
                stock=6,
                is_active=True,
                is_default=False,
            ),
            # Варианты для футбольных бутс (product_id=4)
            ProductVariantEntity(
                id=9,
                product_id=4,
                image_id=None,
                city_id=None,
                title_ru="Футбольные бутсы Adidas Predator - Размер 42",
                title_kk="Adidas Predator футбол бутсалары - 42 өлшем",
                title_en="Adidas Predator Football Boots - Size 42",
                value=DbValueConstants.get_value("Футбольные бутсы Adidas Predator - Размер 42"),
                sku="ADIDAS-PRED-42",
                price_delta=Decimal("0.00"),
                stock=5,
                is_active=True,
                is_default=True,
            ),
            # Варианты для мяча FIFA (product_id=5) - без вариантов, стандартный товар
            ProductVariantEntity(
                id=10,
                product_id=5,
                image_id=None,
                city_id=None,
                title_ru="Мяч футбольный FIFA - Стандартный",
                title_kk="FIFA футбол добы - Стандартты",
                title_en="FIFA Football Ball - Standard",
                value=DbValueConstants.get_value("Мяч футбольный FIFA - Стандартный"),
                sku="FIFA-BALL-STD",
                price_delta=Decimal("0.00"),
                stock=50,
                is_active=True,
                is_default=True,
            ),
            # Варианты для гантелей (product_id=6)
            ProductVariantEntity(
                id=11,
                product_id=6,
                image_id=None,
                city_id=None,
                title_ru="Гантели разборные - Комплект 20кг",
                title_kk="Бөлшектенетін гантельдер - 20кг жинағы",
                title_en="Adjustable Dumbbells - 20kg Set",
                value=DbValueConstants.get_value("Гантели разборные - Комплект 20кг"),
                sku="DUMB-ADJ-20KG-SET",
                price_delta=Decimal("0.00"),
                stock=15,
                is_active=True,
                is_default=True,
            ),
            # Варианты для детского костюма (product_id=7)
            ProductVariantEntity(
                id=12,
                product_id=7,
                image_id=None,
                city_id=None,
                title_ru="Детский спортивный костюм - Размер 110",
                title_kk="Балалар спорт костюмі - 110 өлшем",
                title_en="Kids Sports Suit - Size 110",
                value=DbValueConstants.get_value("Детский спортивный костюм - Размер 110"),
                sku="KIDS-SUIT-110",
                price_delta=Decimal("0.00"),
                stock=20,
                is_active=True,
                is_default=True,
            ),
            ProductVariantEntity(
                id=13,
                product_id=7,
                image_id=None,
                city_id=None,
                title_ru="Детский спортивный костюм - Размер 120",
                title_kk="Балалар спорт костюмі - 120 өлшем",
                title_en="Kids Sports Suit - Size 120",
                value=DbValueConstants.get_value("Детский спортивный костюм - Размер 120"),
                sku="KIDS-SUIT-120",
                price_delta=Decimal("0.00"),
                stock=18,
                is_active=True,
                is_default=False,
            ),
            # Варианты для женских леггинсов (product_id=8)
            ProductVariantEntity(
                id=14,
                product_id=8,
                image_id=None,
                city_id=None,
                title_ru="Женские леггинсы для йоги - Черные S",
                title_kk="Йогаға арналған әйелдер легинстері - Қара S",
                title_en="Women's Yoga Leggings - Black S",
                value=DbValueConstants.get_value("Женские леггинсы для йоги - Черные S"),
                sku="WOMEN-YOGA-BLK-S",
                price_delta=Decimal("0.00"),
                stock=25,
                is_active=True,
                is_default=True,
            ),
            ProductVariantEntity(
                id=15,
                product_id=8,
                image_id=None,
                city_id=None,
                title_ru="Женские леггинсы для йоги - Серые M",
                title_kk="Йогаға арналған әйелдер легинстері - Сұр M",
                title_en="Women's Yoga Leggings - Grey M",
                value=DbValueConstants.get_value("Женские леггинсы для йоги - Серые M"),
                sku="WOMEN-YOGA-GRY-M",
                price_delta=Decimal("0.00"),
                stock=22,
                is_active=True,
                is_default=False,
            ),
        ]

    def get_prod_data(self) -> list[ProductVariantEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass