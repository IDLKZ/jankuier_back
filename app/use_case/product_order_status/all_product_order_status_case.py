from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_status.product_order_status_dto import ProductOrderStatusRDTO, \
    ProductOrderStatusWithRelationsRDTO
from app.adapters.filters.product_order_status.product_order_status_filter import ProductOrderStatusFilter
from app.adapters.repository.product_order_status.product_order_status_repository import ProductOrderStatusRepository
from app.use_case.base_case import BaseUseCase


class AllProductOrderStatusCase(BaseUseCase[list[ProductOrderStatusWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех статусов заказов.

    Использует:
        - Репозиторий `ProductOrderStatusRepository` для работы с базой данных.
        - DTO `ProductOrderStatusRDTO` для возврата данных.

    Атрибуты:
        repository (ProductOrderStatusRepository): Репозиторий для работы со статусами заказов.

    Методы:
        execute() -> list[ProductOrderStatusRDTO]:
            Выполняет запрос и возвращает список всех статусов заказов.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductOrderStatusRepository(db)

    async def execute(self, filter: ProductOrderStatusFilter) -> list[ProductOrderStatusWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех статусов заказов.

        Returns:
            list[ProductOrderStatusRDTO]: Список объектов статусов заказов.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
            options=self.repository.default_relationships(),
        )
        return [ProductOrderStatusRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """