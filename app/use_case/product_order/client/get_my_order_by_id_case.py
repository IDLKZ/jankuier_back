from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order.full_product_order_dto import FullProductOrderRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetMyOrderByIdCase(BaseUseCase[FullProductOrderRDTO]):
    """
    Use Case для получения конкретного заказа пользователя по ID.

    Основная функциональность:
    - Получает заказ по ID, принадлежащий текущему пользователю
    - Проверяет права доступа (заказ должен принадлежать пользователю)
    - Возвращает заказ с полными relationships
    - Поддерживает получение удаленных заказов при необходимости

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        current_user: Текущий пользователь
        order_id: ID заказа для получения
        include_deleted: Флаг включения удаленных записей

    Returns:
        ProductOrderWithRelationsRDTO: Заказ с relationships

    Raises:
        AppExceptionResponse: При отсутствии заказа или нарушении прав доступа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения заказа по ID.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.current_user: UserWithRelationsRDTO | None = None
        self.order_id: int | None = None
        self.include_deleted: bool = False

    async def execute(
        self,
        user: UserWithRelationsRDTO,
        order_id: int,
        include_deleted: bool = False
    ) -> FullProductOrderRDTO:
        """
        Основной метод выполнения получения заказа по ID.

        Получает заказ по ID с проверкой прав доступа.

        Args:
            user (UserWithRelationsRDTO): Текущий пользователь
            order_id (int): ID заказа для получения
            include_deleted (bool, optional): Включать удаленные записи. По умолчанию False.

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с полными relationships

        Raises:
            AppExceptionResponse: При отсутствии заказа или нарушении прав доступа
        """
        self.current_user = user
        self.order_id = order_id
        self.include_deleted = include_deleted

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных и прав доступа.

        Проверяет:
        - Корректность входных параметров
        - Существование заказа
        - Принадлежность заказа текущему пользователю

        Raises:
            AppExceptionResponse: При ошибках валидации или отсутствии прав доступа
        """
        if not self.current_user or not self.order_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        # Получаем заказ с проверкой принадлежности пользователю
        order = await self.product_order_repository.get_first_with_filters(
            filters=[
                self.product_order_repository.model.id == self.order_id,
                self.product_order_repository.model.user_id == self.current_user.id
            ],
            include_deleted_filter=self.include_deleted
        )

        if not order:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_not_found")
            )

    async def transform(self) -> FullProductOrderRDTO:
        """
        Получение и трансформация данных.

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с relationships
        """
        order_items = []
        order = await self.product_order_repository.get_first_with_filters(
            filters=[
                self.product_order_repository.model.id == self.order_id,
                self.product_order_repository.model.user_id == self.current_user.id
            ],
            options=self.product_order_repository.default_relationships(),
            include_deleted_filter=self.include_deleted
        )
        if order:
            order_items = await self.product_order_item_repository.get_with_filters(
                filters=[
                    self.product_order_item_repository.model.order_id == order.id
                ],
                options=self.product_order_item_repository.default_relationships(),
            )
        return FullProductOrderRDTO(
            product_order=ProductOrderWithRelationsRDTO.model_validate(order),
            product_order_items=[ProductOrderItemWithRelationsRDTO.model_validate(item) for item in order_items]
        )