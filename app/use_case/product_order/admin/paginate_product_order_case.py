from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderWithRelationsRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.filters.product_order.product_order_pagination_filter import ProductOrderPaginationFilter
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.use_case.base_case import BaseUseCase


class PaginateProductOrderCase(BaseUseCase[PaginationProductOrderWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка заказов (админ).

    Основная функциональность:
    - Получает все заказы системы с пагинацией
    - Поддерживает фильтрацию по различным критериям
    - Возвращает заказы с полными relationships
    - Доступ только для администраторов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        filter_obj: Объект фильтрации с параметрами поиска и пагинации

    Returns:
        PaginationProductOrderWithRelationsRDTO содержащий список ProductOrderWithRelationsRDTO
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения списка заказов.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.filter_obj: ProductOrderPaginationFilter | None = None

    async def execute(
        self,
        filter_obj: ProductOrderPaginationFilter
    ) -> PaginationProductOrderWithRelationsRDTO:
        """
        Основной метод выполнения получения заказов.

        Получает пагинированный список всех заказов системы с применением фильтров.

        Args:
            filter_obj (ProductOrderPaginationFilter): Объект фильтрации и пагинации

        Returns:
            PaginationProductOrderWithRelationsRDTO: Пагинированный список заказов
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

    async def transform(self) -> PaginationProductOrderWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            PaginationProductOrderWithRelationsRDTO с заказами и relationships
        """
        return await self.product_order_repository.paginate(
            dto=ProductOrderWithRelationsRDTO,
            filters=self.filter_obj.apply(),
            options=self.product_order_repository.default_relationships(),
            order_by=self.filter_obj.order_by,
            order_direction=self.filter_obj.order_direction
        )