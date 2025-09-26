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
                title_ru="Футбольная форма",
                title_kk="Футбол формасы",
                title_en="Football Kit",
                description_ru="Профессиональная футбольная форма для команд и индивидуальных игроков. Игровые и тренировочные комплекты.",
                description_kk="Командалар мен жеке ойыншыларға арналған кәсіби футбол формасы. Ойын және жаттығу жинақтары.",
                description_en="Professional football kits for teams and individual players. Match and training sets.",
                value=DbValueConstants.get_value("Футбольная форма"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=2,
                image_id=None,
                title_ru="Футбольная обувь",
                title_kk="Футбол аяқ киімі",
                title_en="Football Footwear",
                description_ru="Футбольные бутсы, сороконожки, футзалки для различных покрытий и стилей игры.",
                description_kk="Әртүрлі жамылғылар мен ойын стильдеріне арналған футбол бутсалары, сороконожкалар, футзалкалар.",
                description_en="Football boots, turf shoes, futsal shoes for various surfaces and playing styles.",
                value=DbValueConstants.get_value("Футбольная обувь"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=3,
                image_id=None,
                title_ru="Футбольные мячи",
                title_kk="Футбол доптары",
                title_en="Football Balls",
                description_ru="Мячи для футбола, мини-футбола, футзала. Профессиональные, тренировочные и любительские мячи.",
                description_kk="Футбол, мини-футбол, футзалға арналған доптар. Кәсіби, жаттығу және әуесқой доптар.",
                description_en="Balls for football, mini-football, futsal. Professional, training and amateur balls.",
                value=DbValueConstants.get_value("Футбольные мячи"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=4,
                image_id=None,
                title_ru="Тренировочное оборудование",
                title_kk="Жаттығу жабдықтары",
                title_en="Training Equipment",
                description_ru="Конусы, маркеры, барьеры, лестницы для координации, манишки и другое оборудование для футбольных тренировок.",
                description_kk="Конустар, маркерлер, кедергілер, үйлестіру сатылары, манишкалар және футбол жаттығуларына арналған басқа жабдықтар.",
                description_en="Cones, markers, hurdles, coordination ladders, bibs and other equipment for football training.",
                value=DbValueConstants.get_value("Тренировочное оборудование"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=5,
                image_id=None,
                title_ru="Защитная экипировка",
                title_kk="Қорғаныс жабдықтары",
                title_en="Protective Equipment",
                description_ru="Щитки, перчатки вратаря, наколенники, голеностоп и другие средства защиты для футболистов.",
                description_kk="Қалқандар, қақпашы қолғаптары, тізе қорғаушылары, кіші жіліншік және футболшыларға арналған басқа қорғау құралдары.",
                description_en="Shin guards, goalkeeper gloves, knee pads, ankle support and other protective gear for footballers.",
                value=DbValueConstants.get_value("Защитная экипировка"),
                is_active=True,
            ),
            ProductCategoryEntity(
                id=6,
                image_id=None,
                title_ru="Футбольные аксессуары",
                title_kk="Футбол аксессуарлары",
                title_en="Football Accessories",
                description_ru="Сумки, рюкзаки, бутылки для воды, свистки, повязки капитана и другие футбольные аксессуары.",
                description_kk="Сөмкелер, арқа сөмкелер, су бөтелкелері, ысқырықтар, капитан таңғыштары және басқа футбол аксессуарлары.",
                description_en="Bags, backpacks, water bottles, whistles, captain armbands and other football accessories.",
                value=DbValueConstants.get_value("Футбольные аксессуары"),
                is_active=True,
            ),
        ]

    def get_prod_data(self) -> list[ProductCategoryEntity]:
        return self.get_dev_data()

    def get_dev_updated_data(self) -> None:
        pass

    def get_prod_updated_data(self) -> None:
        pass