from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductOrderByIdCase(BaseUseCase[ProductOrderWithRelationsRDTO]):
    """
    Use Case для получения заказа по ID (админ).

    Основная функциональность:
    - Получает заказ по ID
    - Возвращает заказ с полными relationships
    - Поддерживает получение удаленных заказов
    - Доступ только для администраторов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        order_id: ID заказа для получения
        include_deleted: Флаг включения удаленных записей

    Returns:
        ProductOrderWithRelationsRDTO: Заказ с relationships

    Raises:
        AppExceptionResponse: При отсутствии заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения заказа по ID.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.order_id: int | None = None
        self.include_deleted: bool = False

    async def execute(
        self,
        order_id: int,
        include_deleted: bool = False
    ) -> ProductOrderWithRelationsRDTO:
        """
        Основной метод выполнения получения заказа по ID.

        Получает заказ по ID с возможностью включения удаленных записей.

        Args:
            order_id (int): ID заказа для получения
            include_deleted (bool, optional): Включать удаленные записи. По умолчанию False.

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с полными relationships

        Raises:
            AppExceptionResponse: При отсутствии заказа
        """
        self.order_id = order_id
        self.include_deleted = include_deleted

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет существование заказа.

        Raises:
            AppExceptionResponse: При отсутствии заказа
        """
        if not self.order_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        order = await self.product_order_repository.get(
            id=self.order_id,
            include_deleted_filter=self.include_deleted
        )

        if not order:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("product_order_not_found")
            )

    async def transform(self) -> ProductOrderWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с relationships
        """
        order = await self.product_order_repository.get(
            id=self.order_id,
            options=self.product_order_repository.default_relationships(),
            include_deleted_filter=self.include_deleted
        )

        return ProductOrderWithRelationsRDTO.model_validate(order)