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
            # Спортивная одежда (category_id=1)
            ProductEntity(
                id=1,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Футболка Nike Pro",
                title_kk="Nike Pro футболкасы",
                title_en="Nike Pro T-Shirt",
                description_ru="Профессиональная спортивная футболка из дышащего материала",
                description_kk="Тыныс алатын материалдан жасалған кәсіби спорт футболкасы",
                description_en="Professional sports t-shirt made from breathable material",
                value=DbValueConstants.get_value("Футболка Nike Pro"),
                sku="NIKE-PRO-TSHIRT-001",
                base_price=Decimal("5990.00"),
                old_price=Decimal("6990.00"),
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
                title_ru="Спортивный костюм Adidas",
                title_kk="Adidas спорт костюмы",
                title_en="Adidas Sports Suit",
                description_ru="Классический спортивный костюм для тренировок",
                description_kk="Жаттығуларға арналған классикалық спорт костюмі",
                description_en="Classic sports suit for training",
                value=DbValueConstants.get_value("Спортивный костюм Adidas"),
                sku="ADIDAS-SUIT-001",
                base_price=Decimal("18990.00"),
                old_price=None,
                gender=1,  # male
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            # Спортивная обувь (category_id=2)
            ProductEntity(
                id=3,
                image_id=None,
                city_id=None,
                category_id=2,
                title_ru="Кроссовки Nike Air Max",
                title_kk="Nike Air Max кроссовкалары",
                title_en="Nike Air Max Sneakers",
                description_ru="Беговые кроссовки с амортизирующей подошвой",
                description_kk="Амортизациялаушы табанды жүгіру кроссовкалары",
                description_en="Running sneakers with cushioned sole",
                value=DbValueConstants.get_value("Кроссовки Nike Air Max"),
                sku="NIKE-AIRMAX-001",
                base_price=Decimal("24990.00"),
                old_price=Decimal("29990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=4,
                image_id=None,
                city_id=None,
                category_id=2,
                title_ru="Футбольные бутсы Adidas Predator",
                title_kk="Adidas Predator футбол бутсалары",
                title_en="Adidas Predator Football Boots",
                description_ru="Профессиональные футбольные бутсы для игры на траве",
                description_kk="Шөпте ойнауға арналған кәсіби футбол бутсалары",
                description_en="Professional football boots for grass play",
                value=DbValueConstants.get_value("Футбольные бутсы Adidas Predator"),
                sku="ADIDAS-PRED-001",
                base_price=Decimal("32990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            # Спортивное оборудование (category_id=3)
            ProductEntity(
                id=5,
                image_id=None,
                city_id=None,
                category_id=3,
                title_ru="Мяч футбольный FIFA",
                title_kk="FIFA футбол добы",
                title_en="FIFA Football Ball",
                description_ru="Официальный футбольный мяч FIFA для профессиональной игры",
                description_kk="Кәсіби ойынға арналған ресми FIFA футбол добы",
                description_en="Official FIFA football ball for professional play",
                value=DbValueConstants.get_value("Мяч футбольный FIFA"),
                sku="FIFA-BALL-001",
                base_price=Decimal("8990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
            ProductEntity(
                id=6,
                image_id=None,
                city_id=None,
                category_id=3,
                title_ru="Гантели разборные 20кг",
                title_kk="Бөлшектенетін гантельдер 20кг",
                title_en="Adjustable Dumbbells 20kg",
                description_ru="Разборные гантели с регулируемым весом от 2 до 20 кг",
                description_kk="2-ден 20 кг дейін реттелетін салмақты бөлшектенетін гантельдер",
                description_en="Adjustable dumbbells with weight range from 2 to 20 kg",
                value=DbValueConstants.get_value("Гантели разборные 20кг"),
                sku="DUMB-ADJ-20KG",
                base_price=Decimal("15990.00"),
                old_price=Decimal("17990.00"),
                gender=0,  # unisex
                is_for_children=False,
                is_recommended=False,
                is_active=True,
            ),
            # Детские товары
            ProductEntity(
                id=7,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Детский спортивный костюм",
                title_kk="Балалар спорт костюмі",
                title_en="Kids Sports Suit",
                description_ru="Удобный спортивный костюм для детей 6-12 лет",
                description_kk="6-12 жастағы балаларға арналған ыңғайлы спорт костюмі",
                description_en="Comfortable sports suit for children 6-12 years old",
                value=DbValueConstants.get_value("Детский спортивный костюм"),
                sku="KIDS-SUIT-001",
                base_price=Decimal("7990.00"),
                old_price=None,
                gender=0,  # unisex
                is_for_children=True,
                is_recommended=True,
                is_active=True,
            ),
            # Женские товары
            ProductEntity(
                id=8,
                image_id=None,
                city_id=None,
                category_id=1,
                title_ru="Женские леггинсы для йоги",
                title_kk="Йогаға арналған әйелдер легинстері",
                title_en="Women's Yoga Leggings",
                description_ru="Эластичные леггинсы для занятий йогой и фитнесом",
                description_kk="Йога мен фитнеспен айналысуға арналған эластикалы легинстер",
                description_en="Elastic leggings for yoga and fitness",
                value=DbValueConstants.get_value("Женские леггинсы для йоги"),
                sku="WOMEN-YOGA-LEG-001",
                base_price=Decimal("4990.00"),
                old_price=None,
                gender=2,  # female
                is_for_children=False,
                is_recommended=True,
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ProductEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass