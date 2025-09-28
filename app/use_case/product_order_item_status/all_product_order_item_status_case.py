from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item_status.product_order_item_status_dto import ProductOrderItemStatusRDTO, \
    ProductOrderItemStatusWithRelationsRDTO
from app.adapters.filters.product_order_item_status.product_order_item_status_filter import ProductOrderItemStatusFilter
from app.adapters.repository.product_order_item_status.product_order_item_status_repository import ProductOrderItemStatusRepository
from app.use_case.base_case import BaseUseCase


class AllProductOrderItemStatusCase(BaseUseCase[list[ProductOrderItemStatusWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех статусов элементов заказов.

    Использует:
        - Репозиторий `ProductOrderItemStatusRepository` для работы с базой данных.
        - DTO `ProductOrderItemStatusRDTO` для возврата данных.

    Атрибуты:
        repository (ProductOrderItemStatusRepository): Репозиторий для работы со статусами элементов заказов.

    Методы:
        execute() -> list[ProductOrderItemStatusRDTO]:
            Выполняет запрос и возвращает список всех статусов элементов заказов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductOrderItemStatusRepository(db)

    async def execute(self, filter: ProductOrderItemStatusFilter) -> list[ProductOrderItemStatusWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех статусов элементов заказов.

        Returns:
            list[ProductOrderItemStatusRDTO]: Список объектов статусов элементов заказов.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
            options=self.repository.default_relationships(),
        )
        return [ProductOrderItemStatusRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """