from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ModificationValueEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames


class ModificationValueSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        modification_values = self.get_data()
        await self.load_seeders(
            ModificationValueEntity, session, AppTableNames.ModificationValueTableName, modification_values
        )

    def get_dev_data(self) -> list[ModificationValueEntity]:
        return [
            # Значения для Футболки Nike Pro (product_id=1)
            # Размеры (modification_type_id=1)
            ModificationValueEntity(
                id=1,
                modification_type_id=1,  # Размер
                product_id=1,  # Футболка Nike Pro
                title_ru="S",
                title_kk="S",
                title_en="S",
                description_ru="Размер S (46-48)",
                description_kk="S өлшемі (46-48)",
                description_en="Size S (46-48)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=2,
                modification_type_id=1,  # Размер
                product_id=1,  # Футболка Nike Pro
                title_ru="M",
                title_kk="M",
                title_en="M",
                description_ru="Размер M (50-52)",
                description_kk="M өлшемі (50-52)",
                description_en="Size M (50-52)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=3,
                modification_type_id=1,  # Размер
                product_id=1,  # Футболка Nike Pro
                title_ru="L",
                title_kk="L",
                title_en="L",
                description_ru="Размер L (54-56)",
                description_kk="L өлшемі (54-56)",
                description_en="Size L (54-56)",
                is_active=True,
            ),
            # Цвета для Футболки Nike Pro (modification_type_id=2)
            ModificationValueEntity(
                id=4,
                modification_type_id=2,  # Цвет
                product_id=1,  # Футболка Nike Pro
                title_ru="Черный",
                title_kk="Қара",
                title_en="Black",
                description_ru="Классический черный цвет",
                description_kk="Классикалық қара түс",
                description_en="Classic black color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=5,
                modification_type_id=2,  # Цвет
                product_id=1,  # Футболка Nike Pro
                title_ru="Белый",
                title_kk="Ақ",
                title_en="White",
                description_ru="Белый цвет",
                description_kk="Ақ түс",
                description_en="White color",
                is_active=True,
            ),

            # Значения для Спортивного костюма Adidas (product_id=2)
            # Размеры
            ModificationValueEntity(
                id=6,
                modification_type_id=1,  # Размер
                product_id=2,  # Спортивный костюм Adidas
                title_ru="M",
                title_kk="M",
                title_en="M",
                description_ru="Размер M (50-52)",
                description_kk="M өлшемі (50-52)",
                description_en="Size M (50-52)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=7,
                modification_type_id=1,  # Размер
                product_id=2,  # Спортивный костюм Adidas
                title_ru="L",
                title_kk="L",
                title_en="L",
                description_ru="Размер L (54-56)",
                description_kk="L өлшемі (54-56)",
                description_en="Size L (54-56)",
                is_active=True,
            ),
            # Цвет
            ModificationValueEntity(
                id=8,
                modification_type_id=2,  # Цвет
                product_id=2,  # Спортивный костюм Adidas
                title_ru="Синий",
                title_kk="Көк",
                title_en="Blue",
                description_ru="Темно-синий цвет",
                description_kk="Қара-көк түс",
                description_en="Navy blue color",
                is_active=True,
            ),

            # Значения для Кроссовок Nike Air Max (product_id=3)
            # Размеры обуви
            ModificationValueEntity(
                id=9,
                modification_type_id=1,  # Размер
                product_id=3,  # Кроссовки Nike Air Max
                title_ru="42",
                title_kk="42",
                title_en="42",
                description_ru="Размер 42 (27см)",
                description_kk="42 өлшем (27см)",
                description_en="Size 42 (27cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=10,
                modification_type_id=1,  # Размер
                product_id=3,  # Кроссовки Nike Air Max
                title_ru="43",
                title_kk="43",
                title_en="43",
                description_ru="Размер 43 (27.5см)",
                description_kk="43 өлшем (27.5см)",
                description_en="Size 43 (27.5cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=11,
                modification_type_id=1,  # Размер
                product_id=3,  # Кроссовки Nike Air Max
                title_ru="44",
                title_kk="44",
                title_en="44",
                description_ru="Размер 44 (28см)",
                description_kk="44 өлшем (28см)",
                description_en="Size 44 (28cm)",
                is_active=True,
            ),

            # Значения для Футбольных бутс Adidas Predator (product_id=4)
            ModificationValueEntity(
                id=12,
                modification_type_id=1,  # Размер
                product_id=4,  # Футбольные бутсы
                title_ru="42",
                title_kk="42",
                title_en="42",
                description_ru="Размер 42 (27см)",
                description_kk="42 өлшем (27см)",
                description_en="Size 42 (27cm)",
                is_active=True,
            ),

            # Значения для Детского спортивного костюма (product_id=7)
            # Детские размеры
            ModificationValueEntity(
                id=13,
                modification_type_id=1,  # Размер
                product_id=7,  # Детский костюм
                title_ru="110",
                title_kk="110",
                title_en="110",
                description_ru="Рост 110см (6-7 лет)",
                description_kk="110см бойы (6-7 жас)",
                description_en="Height 110cm (6-7 years)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=14,
                modification_type_id=1,  # Размер
                product_id=7,  # Детский костюм
                title_ru="120",
                title_kk="120",
                title_en="120",
                description_ru="Рост 120см (8-9 лет)",
                description_kk="120см бойы (8-9 жас)",
                description_en="Height 120cm (8-9 years)",
                is_active=True,
            ),

            # Значения для Женских леггинсов (product_id=8)
            ModificationValueEntity(
                id=15,
                modification_type_id=1,  # Размер
                product_id=8,  # Женские леггинсы
                title_ru="S",
                title_kk="S",
                title_en="S",
                description_ru="Размер S (42-44)",
                description_kk="S өлшемі (42-44)",
                description_en="Size S (42-44)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=16,
                modification_type_id=1,  # Размер
                product_id=8,  # Женские леггинсы
                title_ru="M",
                title_kk="M",
                title_en="M",
                description_ru="Размер M (46-48)",
                description_kk="M өлшемі (46-48)",
                description_en="Size M (46-48)",
                is_active=True,
            ),
            # Цвета для леггинсов
            ModificationValueEntity(
                id=17,
                modification_type_id=2,  # Цвет
                product_id=8,  # Женские леггинсы
                title_ru="Черный",
                title_kk="Қара",
                title_en="Black",
                description_ru="Черный цвет",
                description_kk="Қара түс",
                description_en="Black color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=18,
                modification_type_id=2,  # Цвет
                product_id=8,  # Женские леггинсы
                title_ru="Серый",
                title_kk="Сұр",
                title_en="Grey",
                description_ru="Серый цвет",
                description_kk="Сұр түс",
                description_en="Grey color",
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ModificationValueEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass