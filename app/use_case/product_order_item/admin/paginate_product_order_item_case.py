from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderItemWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.filters.product_order_item.product_order_item_pagination_filter import ProductOrderItemPaginationFilter
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.use_case.base_case import BaseUseCase


class PaginateProductOrderItemCase(BaseUseCase[PaginationProductOrderItemWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка элементов заказов (админ).

    Основная функциональность:
    - Получает все элементы заказов системы с пагинацией
    - Поддерживает фильтрацию по различным критериям
    - Возвращает элементы с полными relationships
    - Доступ только для администраторов

    Attributes:
        product_order_item_repository: Репозиторий для работы с элементами заказов
        filter_obj: Объект фильтрации с параметрами поиска и пагинации

    Returns:
        PaginationProductOrderItemWithRelationsRDTO содержащий список ProductOrderItemWithRelationsRDTO
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения списка элементов заказов.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.filter_obj: ProductOrderItemPaginationFilter | None = None

    async def execute(
        self,
        filter_obj: ProductOrderItemPaginationFilter
    ) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Основной метод выполнения получения элементов заказов.

        Получает пагинированный список всех элементов заказов системы с применением фильтров.

        Args:
            filter_obj (ProductOrderItemPaginationFilter): Объект фильтрации и пагинации

        Returns:
            PaginationProductOrderItemWithRelationsRDTO: Пагинированный список элементов заказов
        """
        self.filter_obj = filter_obj

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет корректность объекта фильтрации.
        """
        pass  # Базовая валидация, дополнительные проверки при необходимости

    async def transform(self) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            PaginationProductOrderItemWithRelationsRDTO с элементами заказов и relationships
        """
        return await self.product_order_item_repository.paginate(
            dto=ProductOrderItemWithRelationsRDTO,
            filters=self.filter_obj.apply(),
            options=self.product_order_item_repository.default_relationships(),
            order_by=self.filter_obj.order_by,
            order_direction=self.filter_obj.order_direction
        )