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
            # Значения для Игровой формы Nike Dri-FIT (product_id=1)
            # Размеры (modification_type_id=1)
            ModificationValueEntity(
                id=1,
                modification_type_id=1,  # Размер
                product_id=1,
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
                product_id=1,
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
                product_id=1,
                title_ru="L",
                title_kk="L",
                title_en="L",
                description_ru="Размер L (54-56)",
                description_kk="L өлшемі (54-56)",
                description_en="Size L (54-56)",
                is_active=True,
            ),
            # Цвета для Игровой формы Nike Dri-FIT (modification_type_id=2)
            ModificationValueEntity(
                id=4,
                modification_type_id=2,  # Цвет
                product_id=1,
                title_ru="Красный",
                title_kk="Қызыл",
                title_en="Red",
                description_ru="Красный цвет",
                description_kk="Қызыл түс",
                description_en="Red color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=5,
                modification_type_id=2,  # Цвет
                product_id=1,
                title_ru="Синий",
                title_kk="Көк",
                title_en="Blue",
                description_ru="Синий цвет",
                description_kk="Көк түс",
                description_en="Blue color",
                is_active=True,
            ),

            # Значения для Тренировочной формы Adidas (product_id=2)
            # Размеры
            ModificationValueEntity(
                id=6,
                modification_type_id=1,  # Размер
                product_id=2,
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
                product_id=2,
                title_ru="L",
                title_kk="L",
                title_en="L",
                description_ru="Размер L (54-56)",
                description_kk="L өлшемі (54-56)",
                description_en="Size L (54-56)",
                is_active=True,
            ),
            # Цвета
            ModificationValueEntity(
                id=8,
                modification_type_id=2,  # Цвет
                product_id=2,
                title_ru="Черный",
                title_kk="Қара",
                title_en="Black",
                description_ru="Черный цвет",
                description_kk="Қара түс",
                description_en="Black color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=9,
                modification_type_id=2,  # Цвет
                product_id=2,
                title_ru="Белый",
                title_kk="Ақ",
                title_en="White",
                description_ru="Белый цвет",
                description_kk="Ақ түс",
                description_en="White color",
                is_active=True,
            ),

            # Значения для Детской футбольной формы (product_id=3)
            # Возрастные группы (как размеры)
            ModificationValueEntity(
                id=10,
                modification_type_id=1,  # Размер
                product_id=3,
                title_ru="6-8 лет",
                title_kk="6-8 жас",
                title_en="6-8 years",
                description_ru="Для детей 6-8 лет",
                description_kk="6-8 жас балаларға",
                description_en="For kids 6-8 years",
                is_active=True,
            ),
            ModificationValueEntity(
                id=11,
                modification_type_id=1,  # Размер
                product_id=3,
                title_ru="10-12 лет",
                title_kk="10-12 жас",
                title_en="10-12 years",
                description_ru="Для детей 10-12 лет",
                description_kk="10-12 жас балаларға",
                description_en="For kids 10-12 years",
                is_active=True,
            ),
            ModificationValueEntity(
                id=12,
                modification_type_id=1,  # Размер
                product_id=3,
                title_ru="14-16 лет",
                title_kk="14-16 жас",
                title_en="14-16 years",
                description_ru="Для детей 14-16 лет",
                description_kk="14-16 жас балаларға",
                description_en="For kids 14-16 years",
                is_active=True,
            ),

            # Значения для Бутс Nike Mercurial (product_id=4)
            # Размеры обуви
            ModificationValueEntity(
                id=13,
                modification_type_id=1,  # Размер
                product_id=4,
                title_ru="40",
                title_kk="40",
                title_en="40",
                description_ru="Размер 40 (26см)",
                description_kk="40 өлшем (26см)",
                description_en="Size 40 (26cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=14,
                modification_type_id=1,  # Размер
                product_id=4,
                title_ru="42",
                title_kk="42",
                title_en="42",
                description_ru="Размер 42 (27см)",
                description_kk="42 өлшем (27см)",
                description_en="Size 42 (27cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=15,
                modification_type_id=1,  # Размер
                product_id=4,
                title_ru="44",
                title_kk="44",
                title_en="44",
                description_ru="Размер 44 (28см)",
                description_kk="44 өлшем (28см)",
                description_en="Size 44 (28cm)",
                is_active=True,
            ),

            # Значения для Сороконожек Adidas Copa (product_id=5)
            # Размеры обуви
            ModificationValueEntity(
                id=16,
                modification_type_id=1,  # Размер
                product_id=5,
                title_ru="41",
                title_kk="41",
                title_en="41",
                description_ru="Размер 41 (26.5см)",
                description_kk="41 өлшем (26.5см)",
                description_en="Size 41 (26.5cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=17,
                modification_type_id=1,  # Размер
                product_id=5,
                title_ru="43",
                title_kk="43",
                title_en="43",
                description_ru="Размер 43 (27.5см)",
                description_kk="43 өлшем (27.5см)",
                description_en="Size 43 (27.5cm)",
                is_active=True,
            ),

            # Значения для Футзалок Puma Future (product_id=6)
            # Размеры обуви
            ModificationValueEntity(
                id=18,
                modification_type_id=1,  # Размер
                product_id=6,
                title_ru="42",
                title_kk="42",
                title_en="42",
                description_ru="Размер 42 (27см)",
                description_kk="42 өлшем (27см)",
                description_en="Size 42 (27cm)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=19,
                modification_type_id=1,  # Размер
                product_id=6,
                title_ru="44",
                title_kk="44",
                title_en="44",
                description_ru="Размер 44 (28см)",
                description_kk="44 өлшем (28см)",
                description_en="Size 44 (28cm)",
                is_active=True,
            ),

            # Значения для Мяча FIFA Pro Quality (product_id=7)
            # Размеры мяча
            ModificationValueEntity(
                id=20,
                modification_type_id=1,  # Размер
                product_id=7,
                title_ru="Размер 4",
                title_kk="4 өлшем",
                title_en="Size 4",
                description_ru="Размер 4 (для подростков)",
                description_kk="4 өлшем (жасөспірімдерге)",
                description_en="Size 4 (for teens)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=21,
                modification_type_id=1,  # Размер
                product_id=7,
                title_ru="Размер 5",
                title_kk="5 өлшем",
                title_en="Size 5",
                description_ru="Размер 5 (стандартный)",
                description_kk="5 өлшем (стандартты)",
                description_en="Size 5 (standard)",
                is_active=True,
            ),

            # Значения для Тренировочного мяча Select (product_id=8)
            # Размер мяча
            ModificationValueEntity(
                id=22,
                modification_type_id=1,  # Размер
                product_id=8,
                title_ru="Размер 5",
                title_kk="5 өлшем",
                title_en="Size 5",
                description_ru="Размер 5 (стандартный)",
                description_kk="5 өлшем (стандартты)",
                description_en="Size 5 (standard)",
                is_active=True,
            ),

            # Значения для Детского мяча размер 3 (product_id=9)
            # Цвета
            ModificationValueEntity(
                id=23,
                modification_type_id=2,  # Цвет
                product_id=9,
                title_ru="Красный",
                title_kk="Қызыл",
                title_en="Red",
                description_ru="Красный цвет",
                description_kk="Қызыл түс",
                description_en="Red color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=24,
                modification_type_id=2,  # Цвет
                product_id=9,
                title_ru="Синий",
                title_kk="Көк",
                title_en="Blue",
                description_ru="Синий цвет",
                description_kk="Көк түс",
                description_en="Blue color",
                is_active=True,
            ),

            # Значения для Набора конусов (product_id=10)
            # Количество
            ModificationValueEntity(
                id=25,
                modification_type_id=3,  # Количество (предполагаем modification_type_id=3)
                product_id=10,
                title_ru="12 шт",
                title_kk="12 дана",
                title_en="12 pcs",
                description_ru="Набор из 12 конусов",
                description_kk="12 конустан тұратын жинақ",
                description_en="Set of 12 cones",
                is_active=True,
            ),
            ModificationValueEntity(
                id=26,
                modification_type_id=3,  # Количество
                product_id=10,
                title_ru="20 шт",
                title_kk="20 дана",
                title_en="20 pcs",
                description_ru="Набор из 20 конусов",
                description_kk="20 конустан тұратын жинақ",
                description_en="Set of 20 cones",
                is_active=True,
            ),

            # Значения для Лестницы координации (product_id=11)
            # Длина
            ModificationValueEntity(
                id=27,
                modification_type_id=4,  # Длина (предполагаем modification_type_id=4)
                product_id=11,
                title_ru="4 метра",
                title_kk="4 метр",
                title_en="4 meters",
                description_ru="Длина 4 метра",
                description_kk="4 метр ұзындығы",
                description_en="4 meters length",
                is_active=True,
            ),
            ModificationValueEntity(
                id=28,
                modification_type_id=4,  # Длина
                product_id=11,
                title_ru="6 метров",
                title_kk="6 метр",
                title_en="6 meters",
                description_ru="Длина 6 метров",
                description_kk="6 метр ұзындығы",
                description_en="6 meters length",
                is_active=True,
            ),

            # Значения для Щитков Nike Mercurial Lite (product_id=12)
            # Размеры
            ModificationValueEntity(
                id=29,
                modification_type_id=1,  # Размер
                product_id=12,
                title_ru="S",
                title_kk="S",
                title_en="S",
                description_ru="Размер S (малый)",
                description_kk="S өлшемі (кіші)",
                description_en="Size S (small)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=30,
                modification_type_id=1,  # Размер
                product_id=12,
                title_ru="M",
                title_kk="M",
                title_en="M",
                description_ru="Размер M (средний)",
                description_kk="M өлшемі (орташа)",
                description_en="Size M (medium)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=31,
                modification_type_id=1,  # Размер
                product_id=12,
                title_ru="L",
                title_kk="L",
                title_en="L",
                description_ru="Размер L (большой)",
                description_kk="L өлшемі (үлкен)",
                description_en="Size L (large)",
                is_active=True,
            ),

            # Значения для Перчаток вратаря Adidas Predator (product_id=13)
            # Размеры перчаток
            ModificationValueEntity(
                id=32,
                modification_type_id=1,  # Размер
                product_id=13,
                title_ru="Размер 8",
                title_kk="8 өлшем",
                title_en="Size 8",
                description_ru="Размер 8 (малый)",
                description_kk="8 өлшем (кіші)",
                description_en="Size 8 (small)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=33,
                modification_type_id=1,  # Размер
                product_id=13,
                title_ru="Размер 9",
                title_kk="9 өлшем",
                title_en="Size 9",
                description_ru="Размер 9 (средний)",
                description_kk="9 өлшем (орташа)",
                description_en="Size 9 (medium)",
                is_active=True,
            ),
            ModificationValueEntity(
                id=34,
                modification_type_id=1,  # Размер
                product_id=13,
                title_ru="Размер 10",
                title_kk="10 өлшем",
                title_en="Size 10",
                description_ru="Размер 10 (большой)",
                description_kk="10 өлшем (үлкен)",
                description_en="Size 10 (large)",
                is_active=True,
            ),

            # Значения для Сумки спортивной Nike (product_id=14)
            # Цвета
            ModificationValueEntity(
                id=35,
                modification_type_id=2,  # Цвет
                product_id=14,
                title_ru="Черный",
                title_kk="Қара",
                title_en="Black",
                description_ru="Черный цвет",
                description_kk="Қара түс",
                description_en="Black color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=36,
                modification_type_id=2,  # Цвет
                product_id=14,
                title_ru="Синий",
                title_kk="Көк",
                title_en="Blue",
                description_ru="Синий цвет",
                description_kk="Көк түс",
                description_en="Blue color",
                is_active=True,
            ),

            # Значения для Повязки капитана (product_id=15)
            # Цвета
            ModificationValueEntity(
                id=37,
                modification_type_id=2,  # Цвет
                product_id=15,
                title_ru="Красный",
                title_kk="Қызыл",
                title_en="Red",
                description_ru="Красный цвет",
                description_kk="Қызыл түс",
                description_en="Red color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=38,
                modification_type_id=2,  # Цвет
                product_id=15,
                title_ru="Синий",
                title_kk="Көк",
                title_en="Blue",
                description_ru="Синий цвет",
                description_kk="Көк түс",
                description_en="Blue color",
                is_active=True,
            ),
            ModificationValueEntity(
                id=39,
                modification_type_id=2,  # Цвет
                product_id=15,
                title_ru="Желтый",
                title_kk="Сары",
                title_en="Yellow",
                description_ru="Желтый цвет",
                description_kk="Сары түс",
                description_en="Yellow color",
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ModificationValueEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass