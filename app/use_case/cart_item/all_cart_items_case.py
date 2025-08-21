from sqlalchemy import func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import CartItemWithRelationsRDTO
from app.adapters.filter.base_filter import BaseFilter
from app.adapters.repository.cart_item.cart_item_repository import CartItemRepository
from app.use_case.base_case import BaseUseCase


class AllCartItemsCase(BaseUseCase[list[CartItemWithRelationsRDTO]]):
    """
    Класс Use Case для получения всех товаров в корзинах с фильтрацией.

    Использует:
        - Репозиторий `CartItemRepository` для работы с базой данных.
        - Фильтр `BaseFilter` для применения условий поиска и сортировки.
        - DTO `CartItemWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (CartItemRepository): Репозиторий для работы с товарами в корзинах.

    Методы:
        execute(filter: BaseFilter) -> list[CartItemWithRelationsRDTO]:
            Выполняет запрос и возвращает список товаров в корзинах.
        validate(filter: BaseFilter):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CartItemRepository(db)

    async def execute(self, filter: BaseFilter) -> list[CartItemWithRelationsRDTO]:
        """
        Выполняет операцию получения всех товаров в корзинах с фильтрацией.

        Args:
            filter (BaseFilter): Объект фильтра с параметрами поиска и сортировки.

        Returns:
            list[CartItemWithRelationsRDTO]: Список товаров в корзинах с связями.
        """
        await self.validate(filter)

        # Применяем фильтры
        filters = []
        if hasattr(filter, "search") and filter.search:
            search_term = f"%{filter.search.lower()}%"
            # Поиск по SKU, названию товара или цене
            filters.append(
                or_(
                    func.lower(self.repository.model.sku).like(search_term),
                    func.lower(self.repository.model.product.title_ru).like(
                        search_term
                    ),
                    func.lower(self.repository.model.product.title_kk).like(
                        search_term
                    ),
                    func.lower(self.repository.model.product.title_en).like(
                        search_term
                    ),
                    func.cast(self.repository.model.unit_price, func.text("TEXT")).like(
                        search_term
                    ),
                    func.cast(
                        self.repository.model.total_price, func.text("TEXT")
                    ).like(search_term),
                    func.cast(self.repository.model.qty, func.text("TEXT")).like(
                        search_term
                    ),
                )
            )

        # Получаем данные из репозитория
        models = await self.repository.get_with_filters(
            filters=filters,
            order_by=getattr(filter, "order_by", "created_at"),
            order_direction=getattr(filter, "order_direction", "desc"),
            include_deleted_filter=not getattr(filter, "is_show_deleted", False),
            options=self.repository.default_relationships(),
        )

        return [CartItemWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self, filter: BaseFilter) -> None:
        """
        Валидация входных параметров.

        Args:
            filter (BaseFilter): Фильтр для валидации.
        """
        pass

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
