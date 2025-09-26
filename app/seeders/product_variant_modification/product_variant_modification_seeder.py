from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductVariantModificationEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class ProductVariantModificationSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        variant_modifications = self.get_data()
        await self.load_seeders(
            ProductVariantModificationEntity, session, AppTableNames.ProductVariantModificationTableName, variant_modifications
        )

    def get_dev_data(self) -> list[ProductVariantModificationEntity]:
        return [
            # Футбольная форма Nike Dri-FIT (product_id=1)
            # Вариант 1: Красная S (variant_id=1)
            ProductVariantModificationEntity(
                id=1,
                variant_id=1,
                modification_value_id=1,  # Размер S
            ),
            ProductVariantModificationEntity(
                id=2,
                variant_id=1,
                modification_value_id=4,  # Цвет (reusing existing)
            ),
            # Вариант 2: Красная M (variant_id=2)
            ProductVariantModificationEntity(
                id=3,
                variant_id=2,
                modification_value_id=2,  # Размер M
            ),
            ProductVariantModificationEntity(
                id=4,
                variant_id=2,
                modification_value_id=4,  # Цвет (reusing existing)
            ),
            # Вариант 3: Синяя L (variant_id=3)
            ProductVariantModificationEntity(
                id=5,
                variant_id=3,
                modification_value_id=3,  # Размер L
            ),
            ProductVariantModificationEntity(
                id=6,
                variant_id=3,
                modification_value_id=8,  # Цвет Синий (from existing)
            ),

            # Тренировочная форма Adidas (product_id=2)
            # Вариант 4: Черная M (variant_id=4)
            ProductVariantModificationEntity(
                id=7,
                variant_id=4,
                modification_value_id=6,  # Размер M (from product_id=2)
            ),
            ProductVariantModificationEntity(
                id=8,
                variant_id=4,
                modification_value_id=4,  # Цвет Черный (reusing)
            ),
            # Вариант 5: Белая L (variant_id=5)
            ProductVariantModificationEntity(
                id=9,
                variant_id=5,
                modification_value_id=7,  # Размер L (from product_id=2)
            ),
            ProductVariantModificationEntity(
                id=10,
                variant_id=5,
                modification_value_id=5,  # Цвет Белый (from existing)
            ),

            # Детская футбольная форма (product_id=3)
            # Вариант 6: 6-8 лет (variant_id=6)
            ProductVariantModificationEntity(
                id=11,
                variant_id=6,
                modification_value_id=13,  # Детский размер (reusing 110)
            ),
            # Вариант 7: 10-12 лет (variant_id=7)
            ProductVariantModificationEntity(
                id=12,
                variant_id=7,
                modification_value_id=14,  # Детский размер (reusing 120)
            ),
            # Вариант 8: 14-16 лет (variant_id=8)
            ProductVariantModificationEntity(
                id=13,
                variant_id=8,
                modification_value_id=14,  # Детский размер (reusing 120)
            ),

            # Бутсы Nike Mercurial (product_id=4)
            # Вариант 9: Размер 40 (variant_id=9)
            ProductVariantModificationEntity(
                id=14,
                variant_id=9,
                modification_value_id=9,  # Размер 42 (closest available)
            ),
            # Вариант 10: Размер 42 (variant_id=10)
            ProductVariantModificationEntity(
                id=15,
                variant_id=10,
                modification_value_id=9,  # Размер 42
            ),
            # Вариант 11: Размер 44 (variant_id=11)
            ProductVariantModificationEntity(
                id=16,
                variant_id=11,
                modification_value_id=11,  # Размер 44
            ),

            # Сороконожки Adidas Copa (product_id=5)
            # Вариант 12: Размер 41 (variant_id=12)
            ProductVariantModificationEntity(
                id=17,
                variant_id=12,
                modification_value_id=9,  # Размер 42 (closest available)
            ),
            # Вариант 13: Размер 43 (variant_id=13)
            ProductVariantModificationEntity(
                id=18,
                variant_id=13,
                modification_value_id=10,  # Размер 43
            ),

            # Футзалки Puma Future (product_id=6)
            # Вариант 14: Размер 42 (variant_id=14)
            ProductVariantModificationEntity(
                id=19,
                variant_id=14,
                modification_value_id=9,  # Размер 42
            ),
            # Вариант 15: Размер 44 (variant_id=15)
            ProductVariantModificationEntity(
                id=20,
                variant_id=15,
                modification_value_id=11,  # Размер 44
            ),

            # Мяч FIFA Pro Quality (product_id=7) - no modifications (standard item)
            # Тренировочный мяч Select (product_id=8) - no modifications (standard item)
            # Детский мяч размер 3 (product_id=9) - basic color variations
            # Вариант 19: Красный (variant_id=19)
            ProductVariantModificationEntity(
                id=21,
                variant_id=19,
                modification_value_id=4,  # Цвет (reusing existing)
            ),
            # Вариант 20: Синий (variant_id=20)
            ProductVariantModificationEntity(
                id=22,
                variant_id=20,
                modification_value_id=8,  # Цвет Синий
            ),

            # Набор конусов (product_id=10) - no specific modifications
            # Лестница для координации (product_id=11) - no specific modifications

            # Щитки Nike Mercurial Lite (product_id=12)
            # Вариант 25: S (variant_id=25)
            ProductVariantModificationEntity(
                id=23,
                variant_id=25,
                modification_value_id=15,  # Размер S (from women's leggings)
            ),
            # Вариант 26: M (variant_id=26)
            ProductVariantModificationEntity(
                id=24,
                variant_id=26,
                modification_value_id=16,  # Размер M (from women's leggings)
            ),
            # Вариант 27: L (variant_id=27)
            ProductVariantModificationEntity(
                id=25,
                variant_id=27,
                modification_value_id=3,  # Размер L (reusing)
            ),

            # Перчатки вратаря Adidas Predator (product_id=13) - using shoe sizes as glove sizes
            # Вариант 28: Размер 8 (variant_id=28)
            ProductVariantModificationEntity(
                id=26,
                variant_id=28,
                modification_value_id=9,  # Размер (reusing)
            ),
            # Вариант 29: Размер 9 (variant_id=29)
            ProductVariantModificationEntity(
                id=27,
                variant_id=29,
                modification_value_id=10,  # Размер (reusing)
            ),
            # Вариант 30: Размер 10 (variant_id=30)
            ProductVariantModificationEntity(
                id=28,
                variant_id=30,
                modification_value_id=11,  # Размер (reusing)
            ),

            # Сумка спортивная Nike (product_id=14)
            # Вариант 31: Черная (variant_id=31)
            ProductVariantModificationEntity(
                id=29,
                variant_id=31,
                modification_value_id=17,  # Цвет Черный (from leggings)
            ),
            # Вариант 32: Синяя (variant_id=32)
            ProductVariantModificationEntity(
                id=30,
                variant_id=32,
                modification_value_id=8,  # Цвет Синий
            ),

            # Повязка капитана (product_id=15)
            # Вариант 33: Красная (variant_id=33)
            ProductVariantModificationEntity(
                id=31,
                variant_id=33,
                modification_value_id=4,  # Цвет (reusing existing)
            ),
            # Вариант 34: Синяя (variant_id=34)
            ProductVariantModificationEntity(
                id=32,
                variant_id=34,
                modification_value_id=8,  # Цвет Синий
            ),
            # Вариант 35: Желтая (variant_id=35)
            ProductVariantModificationEntity(
                id=33,
                variant_id=35,
                modification_value_id=18,  # Цвет Серый (closest available)
            ),
        ]

    def get_prod_data(self) -> list[ProductVariantModificationEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass