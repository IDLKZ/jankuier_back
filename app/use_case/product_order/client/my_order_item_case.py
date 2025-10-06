from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderItemWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.product_order_item.product_order_item_pagination_filter import ProductOrderItemPaginationFilter
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class MyOrderItemCase(BaseUseCase[PaginationProductOrderItemWithRelationsRDTO]):
    """
    Use Case для получения пагинированного списка элементов заказа пользователя.

    Основная функциональность:
    - Получает элементы конкретного заказа, принадлежащего пользователю
    - Проверяет права доступа (заказ должен принадлежать пользователю)
    - Поддерживает фильтрацию и сортировку элементов
    - Возвращает элементы заказа с полными relationships
    - Обеспечивает пагинацию результатов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        product_order_item_repository: Репозиторий для работы с элементами заказа
        current_user: Текущий пользователь
        order_id: ID заказа для получения элементов
        filter_obj: Объект фильтрации с параметрами поиска и пагинации

    Returns:
        PaginationProductOrderItemWithRelationsRDTO содержащий список ProductOrderItemWithRelationsRDTO

    Raises:
        AppExceptionResponse: При отсутствии заказа или нарушении прав доступа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения элементов заказа пользователя.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.current_user: UserWithRelationsRDTO | None = None
        self.order_id: int | None = None
        self.filter_obj: ProductOrderItemPaginationFilter | None = None

    async def execute(
        self,
        user: UserWithRelationsRDTO,
        order_id: int,
        filter_obj: ProductOrderItemPaginationFilter
    ) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Основной метод выполнения получения элементов заказа.

        Получает пагинированный список элементов заказа с проверкой прав доступа.

        Args:
            user (UserWithRelationsRDTO): Текущий пользователь
            order_id (int): ID заказа для получения элементов
            filter_obj (ProductOrderItemPaginationFilter): Объект фильтрации и пагинации

        Returns:
            PaginationProductOrderItemWithRelationsRDTO: Пагинированный список элементов заказа

        Raises:
            AppExceptionResponse: При отсутствии заказа или нарушении прав доступа
        """
        self.current_user = user
        self.order_id = order_id
        self.filter_obj = filter_obj

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных и прав доступа.

        Проверяет:
        - Корректность входных параметров
        - Существование заказа
        - Принадлежность заказа текущему пользователю
        - Добавляет фильтр по order_id для безопасности

        Raises:
            AppExceptionResponse: При ошибках валидации или отсутствии прав доступа
        """
        if not self.current_user or not self.order_id or not self.filter_obj:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        # Проверяем, что заказ существует и принадлежит пользователю
        order = await self.product_order_repository.get_first_with_filters(
            filters=[
                self.product_order_repository.model.id == self.order_id,
                self.product_order_repository.model.user_id == self.current_user.id
            ]
        )

        if not order:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_not_found")
            )

        # Принудительно добавляем фильтр по заказу для безопасности
        self.filter_obj.order_ids = [self.order_id]

    async def transform(self) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            PaginationProductOrderItemWithRelationsRDTO с элементами заказа и relationships
        """
        return await self.product_order_item_repository.paginate(
            dto=ProductOrderItemWithRelationsRDTO,
            filters=self.filter_obj.apply(),
            options=self.product_order_item_repository.default_relationships(),
            order_by=self.filter_obj.order_by,
            order_direction=self.filter_obj.order_direction
        )