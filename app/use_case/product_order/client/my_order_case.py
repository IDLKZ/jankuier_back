from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderWithRelationsRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.product_order.product_order_pagination_filter import ProductOrderPaginationFilter
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.use_case.base_case import BaseUseCase


class MyOrderCase(BaseUseCase[PaginationProductOrderWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка заказов текущего пользователя.

    Основная функциональность:
    - Получает заказы, принадлежащие текущему пользователю
    - Поддерживает фильтрацию и сортировку
    - Возвращает заказы с полными relationships
    - Обеспечивает пагинацию результатов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        current_user: Текущий пользователь
        filter_obj: Объект фильтрации с параметрами поиска и пагинации

    Returns:
        PaginationProductOrderWithRelationsRDTO содержащий список ProductOrderWithRelationsRDTO
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения списка заказов пользователя.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.current_user: UserWithRelationsRDTO | None = None
        self.filter_obj: ProductOrderPaginationFilter | None = None

    async def execute(
        self,
        user: UserWithRelationsRDTO,
        filter_obj: ProductOrderPaginationFilter
    ) -> PaginationProductOrderWithRelationsRDTO:
        """
        Основной метод выполнения получения заказов пользователя.

        Получает пагинированный список заказов текущего пользователя с применением фильтров.

        Args:
            user (UserWithRelationsRDTO): Текущий пользователь
            filter_obj (ProductOrderPaginationFilter): Объект фильтрации и пагинации

        Returns:
            PaginationProductOrderWithRelationsRDTO: Пагинированный список заказов

        Note:
            Автоматически добавляет фильтр по user_id для безопасности,
            чтобы пользователь видел только свои заказы.
        """
        self.current_user = user
        self.filter_obj = filter_obj

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет корректность пользователя и добавляет фильтр по user_id
        для обеспечения безопасности доступа только к собственным заказам.
        """
        if self.current_user and self.filter_obj:
            # Принудительно добавляем фильтр по текущему пользователю для безопасности
            self.filter_obj.user_ids = [self.current_user.id]

    async def transform(self) -> PaginationProductOrderWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            PaginationProductOrderWithRelationsRDTO с заказами пользователя и relationships
        """
        return await self.product_order_repository.paginate(
            dto=ProductOrderWithRelationsRDTO,
            filters=self.filter_obj.apply(),
            options=self.product_order_repository.default_relationships(),
            order_by=self.filter_obj.order_by,
            order_direction=self.filter_obj.order_direction
        )