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
            # Связки для Футболки Nike Pro
            # Вариант 1: Черная S (variant_id=1)
            ProductVariantModificationEntity(
                id=1,
                variant_id=1,
                modification_value_id=1,  # Размер S
            ),
            ProductVariantModificationEntity(
                id=2,
                variant_id=1,
                modification_value_id=4,  # Цвет Черный
            ),
            # Вариант 2: Черная M (variant_id=2)
            ProductVariantModificationEntity(
                id=3,
                variant_id=2,
                modification_value_id=2,  # Размер M
            ),
            ProductVariantModificationEntity(
                id=4,
                variant_id=2,
                modification_value_id=4,  # Цвет Черный
            ),
            # Вариант 3: Белая S (variant_id=3)
            ProductVariantModificationEntity(
                id=5,
                variant_id=3,
                modification_value_id=1,  # Размер S
            ),
            ProductVariantModificationEntity(
                id=6,
                variant_id=3,
                modification_value_id=5,  # Цвет Белый
            ),

            # Связки для Спортивного костюма Adidas
            # Вариант 4: Синий M (variant_id=4)
            ProductVariantModificationEntity(
                id=7,
                variant_id=4,
                modification_value_id=6,  # Размер M
            ),
            ProductVariantModificationEntity(
                id=8,
                variant_id=4,
                modification_value_id=8,  # Цвет Синий
            ),
            # Вариант 5: Синий L (variant_id=5)
            ProductVariantModificationEntity(
                id=9,
                variant_id=5,
                modification_value_id=7,  # Размер L
            ),
            ProductVariantModificationEntity(
                id=10,
                variant_id=5,
                modification_value_id=8,  # Цвет Синий
            ),

            # Связки для кроссовок Nike Air Max
            # Вариант 6: Размер 42 (variant_id=6)
            ProductVariantModificationEntity(
                id=11,
                variant_id=6,
                modification_value_id=9,  # Размер 42
            ),
            # Вариант 7: Размер 43 (variant_id=7)
            ProductVariantModificationEntity(
                id=12,
                variant_id=7,
                modification_value_id=10,  # Размер 43
            ),
            # Вариант 8: Размер 44 (variant_id=8)
            ProductVariantModificationEntity(
                id=13,
                variant_id=8,
                modification_value_id=11,  # Размер 44
            ),

            # Связки для футбольных бутс Adidas Predator
            # Вариант 9: Размер 42 (variant_id=9)
            ProductVariantModificationEntity(
                id=14,
                variant_id=9,
                modification_value_id=12,  # Размер 42
            ),

            # Вариант 10: Мяч FIFA - без модификаций (стандартный товар)
            # Нет записей, так как это стандартный товар без вариаций

            # Вариант 11: Гантели - без модификаций (стандартный товар)
            # Нет записей, так как это стандартный товар без вариаций

            # Связки для детского спортивного костюма
            # Вариант 12: Размер 110 (variant_id=12)
            ProductVariantModificationEntity(
                id=15,
                variant_id=12,
                modification_value_id=13,  # Размер 110
            ),
            # Вариант 13: Размер 120 (variant_id=13)
            ProductVariantModificationEntity(
                id=16,
                variant_id=13,
                modification_value_id=14,  # Размер 120
            ),

            # Связки для женских леггинсов
            # Вариант 14: Черные S (variant_id=14)
            ProductVariantModificationEntity(
                id=17,
                variant_id=14,
                modification_value_id=15,  # Размер S
            ),
            ProductVariantModificationEntity(
                id=18,
                variant_id=14,
                modification_value_id=17,  # Цвет Черный
            ),
            # Вариант 15: Серые M (variant_id=15)
            ProductVariantModificationEntity(
                id=19,
                variant_id=15,
                modification_value_id=16,  # Размер M
            ),
            ProductVariantModificationEntity(
                id=20,
                variant_id=15,
                modification_value_id=18,  # Цвет Серый
            ),
        ]

    def get_prod_data(self) -> list[ProductVariantModificationEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass