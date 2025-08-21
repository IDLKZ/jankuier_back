from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.filters.product.product_filter import ProductFilter
from app.adapters.repository.product.product_repository import ProductRepository
from app.use_case.base_case import BaseUseCase


class AllProductCase(BaseUseCase[list[ProductWithRelationsRDTO]]):
    """
    Класс Use Case для получения списка всех товаров.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - DTO `ProductWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.

    Методы:
        execute(filter: ProductFilter) -> list[ProductWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех товаров.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)

    async def execute(self, filter: ProductFilter) -> list[ProductWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех товаров.

        Args:
            filter (ProductFilter): Фильтр для поиска и сортировки товаров.

        Returns:
            list[ProductWithRelationsRDTO]: Список объектов товаров с отношениями.
        """
        models = await self.repository.get_with_filters(
            filters=filter.apply(),
            options=self.repository.default_relationships(),
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            include_deleted_filter=filter.is_show_deleted,
        )
        return [ProductWithRelationsRDTO.from_orm(model) for model in models]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """