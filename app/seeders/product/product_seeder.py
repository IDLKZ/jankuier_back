from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import ProductEntity
from app.seeders.base_seeder import BaseSeeder
from app.shared.db_table_constants import AppTableNames
from app.shared.db_value_constants import DbValueConstants


class ProductSeeder(BaseSeeder):
    async def seed(self, session: AsyncSession) -> None:
        products = self.get_data()
        await self.load_seeders(
            ProductEntity, session, AppTableNames.ProductTableName, products
        )

    def get_dev_data(self) -> list[ProductEntity]:
        return [
            # Футбольная форма (category_id=1)
            ProductEntity(
                id=1,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Игровая форма Nike Dri-FIT",
                title_kk="Nike Dri-FIT ойын формасы",
                title_en="Nike Dri-FIT Match Kit",
                description_ru="Профессиональная игровая форма с технологией отведения влаги. Комплект: футболка, шорты, гетры.",
                description_kk="Ылғалды шығару технологиясы бар кәсіби ойын формасы. Жинақ: футболка, шорт, ұзын шұлық.",
                description_en="Professional match kit with moisture-wicking technology. Set includes: jersey, shorts, socks.",
                value=DbValueConstants.get_value("Игровая форма Nike Dri-FIT"),
                sku="NIKE-KIT-DRIFIT-001",
                base_price=Decimal("8990.00"),
                old_price=Decimal("10990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=2,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Тренировочная форма Adidas",
                title_kk="Adidas жаттығу формасы",
                title_en="Adidas Training Kit",
                description_ru="Удобная тренировочная форма для ежедневных занятий. Дышащий материал, эргономичный крой.",
                description_kk="Күнделікті жаттығуларға арналған ыңғайлы жаттығу формасы. Тыныс алатын материал, эргономикалық кесім.",
                description_en="Comfortable training kit for daily practice. Breathable material, ergonomic cut.",
                value=DbValueConstants.get_value("Тренировочная форма Adidas"),
                sku="ADIDAS-TRAIN-001",
                base_price=Decimal("6990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=3,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Детская футбольная форма",
                title_kk="Балалар футбол формасы",
                title_en="Kids Football Kit",
                description_ru="Яркая и удобная футбольная форма для юных игроков. Размеры от 6 до 16 лет.",
                description_kk="Жас ойыншыларға арналған жарқын және ыңғайлы футбол формасы. 6-дан 16 жасқа дейінгі өлшемдер.",
                description_en="Bright and comfortable football kit for young players. Sizes from 6 to 16 years.",
                value=DbValueConstants.get_value("Детская футбольная форма"),
                sku="KIDS-FOOTBALL-KIT-001",
                base_price=Decimal("4990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=True,
                is_recommended=True,
                is_active=True,
            ),

            # Футбольная обувь (category_id=2)
            ProductEntity(
                id=4,
                image_id=None,
                city_id=None,
                category_id=2,
                title_ru="Бутсы Nike Mercurial",
                title_kk="Nike Mercurial бутсалары",
                title_en="Nike Mercurial Football Boots",
                description_ru="Профессиональные бутсы для игры на натуральном газоне. Легкие, с отличным сцеплением.",
                description_kk="Табиғи шөпте ойнауға арналған кәсіби бутсалар. Жеңіл, тамаша ұстамға ие.",
                description_en="Professional boots for natural grass play. Lightweight with excellent grip.",
                value=DbValueConstants.get_value("Бутсы Nike Mercurial"),
                sku="NIKE-MERCURIAL-001",
                base_price=Decimal("34990.00"),
                old_price=Decimal("39990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=5,
                image_id=None,
                city_id=None,
                category_id=2,
                title_ru="Сороконожки Adidas Copa",
                title_kk="Adidas Copa сороконожкалары",
                title_en="Adidas Copa Turf Shoes",
                description_ru="Многошиповки для игры на искусственном покрытии. Комфорт и долговечность.",
                description_kk="Жасанды жамылғыда ойнауға арналған көп тіректі аяқ киім. Жайлылық пен ұзақ мерзімділік.",
                description_en="Multi-stud shoes for artificial surface play. Comfort and durability.",
                value=DbValueConstants.get_value("Сороконожки Adidas Copa"),
                sku="ADIDAS-COPA-TURF-001",
                base_price=Decimal("18990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            ProductEntity(
                id=6,
                image_id=None,
                city_id=None,
                category_id=2,
                title_ru="Футзалки Puma Future",
                title_kk="Puma Future футзалкалары",
                title_en="Puma Future Futsal Shoes",
                description_ru="Специализированная обувь для игры в зале. Нескользящая подошва, отличный контроль мяча.",
                description_kk="Залда ойнауға арналған мамандандырылған аяқ киім. Сырғымайтын табан, допты керемет басқару.",
                description_en="Specialized footwear for indoor play. Non-slip sole, excellent ball control.",
                value=DbValueConstants.get_value("Футзалки Puma Future"),
                sku="PUMA-FUTURE-FUTSAL-001",
                base_price=Decimal("22990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),

            # Футбольные мячи (category_id=3)
            ProductEntity(
                id=7,
                image_id=None,
                city_id=None,
                category_id=3,
                title_ru="Мяч FIFA Pro Quality",
                title_kk="FIFA Pro Quality добы",
                title_en="FIFA Pro Quality Ball",
                description_ru="Официальный мяч FIFA качества Pro. Используется в профессиональных турнирах.",
                description_kk="FIFA Pro сапасындағы ресми доп. Кәсіби турнирлерде қолданылады.",
                description_en="Official FIFA Pro quality ball. Used in professional tournaments.",
                value=DbValueConstants.get_value("Мяч FIFA Pro Quality"),
                sku="FIFA-PRO-BALL-001",
                base_price=Decimal("12990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=8,
                image_id=None,
                city_id=None,
                category_id=3,
                title_ru="Тренировочный мяч Select",
                title_kk="Select жаттығу добы",
                title_en="Select Training Ball",
                description_ru="Качественный тренировочный мяч для ежедневных занятий. Прочный и надежный.",
                description_kk="Күнделікті жаттығуларға арналған сапалы жаттығу добы. Берік және сенімді.",
                description_en="Quality training ball for daily practice. Durable and reliable.",
                value=DbValueConstants.get_value("Тренировочный мяч Select"),
                sku="SELECT-TRAIN-BALL-001",
                base_price=Decimal("4990.00"),
                old_price=Decimal("5990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            ProductEntity(
                id=9,
                image_id=None,
                city_id=None,
                category_id=3,
                title_ru="Детский мяч размер 3",
                title_kk="Балалар добы 3 өлшем",
                title_en="Kids Ball Size 3",
                description_ru="Облегченный мяч размер 3 для детей до 12 лет. Яркие цвета, мягкий на ощупь.",
                description_kk="12 жасқа дейінгі балаларға арналған 3 өлшемді жеңілдетілген доп. Жарқын түстер, жұмсақ сезім.",
                description_en="Lightweight size 3 ball for children under 12. Bright colors, soft touch.",
                value=DbValueConstants.get_value("Детский мяч размер 3"),
                sku="KIDS-BALL-SIZE3-001",
                base_price=Decimal("2990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=True,
                is_recommended=True,
                is_active=True,
            ),

            # Тренировочное оборудование (category_id=4)
            ProductEntity(
                id=10,
                image_id=None,
                city_id=None,
                category_id=4,
                title_ru="Набор конусов тренировочных",
                title_kk="Жаттығу конустары жинағы",
                title_en="Training Cones Set",
                description_ru="Комплект из 20 ярких конусов для разметки тренировочных упражнений. Высота 23см.",
                description_kk="Жаттығу жаттығуларын белгілеуге арналған 20 жарқын конус жинағы. Биіктігі 23см.",
                description_en="Set of 20 bright cones for marking training exercises. Height 23cm.",
                value=DbValueConstants.get_value("Набор конусов тренировочных"),
                sku="TRAIN-CONES-SET-20",
                base_price=Decimal("3990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            ProductEntity(
                id=11,
                image_id=None,
                city_id=None,
                category_id=4,
                title_ru="Лестница для координации",
                title_kk="Үйлестіру сатысы",
                title_en="Coordination Ladder",
                description_ru="Тренировочная лестница 6 метров для развития координации, скорости и ловкости.",
                description_kk="Үйлестіруді, жылдамдықты және ептілікті дамытуға арналған 6 метрлік жаттығу сатысы.",
                description_en="6-meter training ladder for developing coordination, speed and agility.",
                value=DbValueConstants.get_value("Лестница для координации"),
                sku="COORD-LADDER-6M",
                base_price=Decimal("5990.00"),
                old_price=Decimal("7990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),

            # Защитная экипировка (category_id=5)
            ProductEntity(
                id=12,
                image_id=None,
                city_id=None,
                category_id=5,
                title_ru="Щитки Nike Mercurial Lite",
                title_kk="Nike Mercurial Lite қалқандары",
                title_en="Nike Mercurial Lite Shin Guards",
                description_ru="Легкие и прочные щитки с анатомической формой. Надежная защита голени.",
                description_kk="Анатомиялық пішіні бар жеңіл және берік қалқандар. Кіші жіліншіктің сенімді қорғанысы.",
                description_en="Lightweight and durable shin guards with anatomical shape. Reliable shin protection.",
                value=DbValueConstants.get_value("Щитки Nike Mercurial Lite"),
                sku="NIKE-SHIN-MERC-LITE",
                base_price=Decimal("2990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=13,
                image_id=None,
                city_id=None,
                category_id=5,
                title_ru="Перчатки вратаря Adidas Predator",
                title_kk="Adidas Predator қақпашы қолғаптары",
                title_en="Adidas Predator Goalkeeper Gloves",
                description_ru="Профессиональные вратарские перчатки с отличным сцеплением и защитой пальцев.",
                description_kk="Керемет ұстамға және саусақтарды қорғауға ие кәсіби қақпашы қолғаптары.",
                description_en="Professional goalkeeper gloves with excellent grip and finger protection.",
                value=DbValueConstants.get_value("Перчатки вратаря Adidas Predator"),
                sku="ADIDAS-GK-PRED-001",
                base_price=Decimal("8990.00"),
                old_price=Decimal("11990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),

            # Футбольные аксессуары (category_id=6)
            ProductEntity(
                id=14,
                image_id=None,
                city_id=None,
                category_id=6,
                title_ru="Сумка спортивная Nike",
                title_kk="Nike спорт сөмкесі",
                title_en="Nike Sports Bag",
                description_ru="Вместительная спортивная сумка для экипировки. Отделения для обуви и формы.",
                description_kk="Жабдықтарға арналған кең спорт сөмкесі. Аяқ киім мен форма үшін бөлімдер.",
                description_en="Spacious sports bag for equipment. Compartments for shoes and kit.",
                value=DbValueConstants.get_value("Сумка спортивная Nike"),
                sku="NIKE-SPORTS-BAG-001",
                base_price=Decimal("6990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            ProductEntity(
                id=15,
                image_id=None,
                city_id=None,
                category_id=6,
                title_ru="Повязка капитана",
                title_kk="Капитан таңғышы",
                title_en="Captain Armband",
                description_ru="Эластичная повязка капитана с надписью 'CAPTAIN'. Подходит для любой окружности руки.",
                description_kk="'CAPTAIN' жазуы бар серпімді капитан таңғышы. Кез келген қол айналымына сәйкес келеді.",
                description_en="Elastic captain armband with 'CAPTAIN' inscription. Fits any arm circumference.",
                value=DbValueConstants.get_value("Повязка капитана"),
                sku="CAPTAIN-ARMBAND-001",
                base_price=Decimal("990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ProductEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass