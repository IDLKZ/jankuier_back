from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductOrderItemByIdCase(BaseUseCase[ProductOrderItemWithRelationsRDTO]):
    """
    Use Case для получения элемента заказа по ID (админ).

    Основная функциональность:
    - Получает элемент заказа по ID
    - Возвращает элемент с полными relationships
    - Поддерживает получение удаленных элементов
    - Доступ только для администраторов

    Attributes:
        product_order_item_repository: Репозиторий для работы с элементами заказов
        item_id: ID элемента заказа для получения
        include_deleted: Флаг включения удаленных записей

    Returns:
        ProductOrderItemWithRelationsRDTO: Элемент заказа с relationships

    Raises:
        AppExceptionResponse: При отсутствии элемента заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для получения элемента заказа по ID.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.item_id: int | None = None
        self.include_deleted: bool = False

    async def execute(
        self,
        item_id: int,
        include_deleted: bool = False
    ) -> ProductOrderItemWithRelationsRDTO:
        """
        Основной метод выполнения получения элемента заказа по ID.

        Получает элемент заказа по ID с возможностью включения удаленных записей.

        Args:
            item_id (int): ID элемента заказа для получения
            include_deleted (bool, optional): Включать удаленные записи. По умолчанию False.

        Returns:
            ProductOrderItemWithRelationsRDTO: Элемент заказа с полными relationships

        Raises:
            AppExceptionResponse: При отсутствии элемента заказа
        """
        self.item_id = item_id
        self.include_deleted = include_deleted

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет существование элемента заказа.

        Raises:
            AppExceptionResponse: При отсутствии элемента заказа
        """
        if not self.item_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        item = await self.product_order_item_repository.get(
            id=self.item_id,
            include_deleted_filter=self.include_deleted
        )

        if not item:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_not_found")
            )

    async def transform(self) -> ProductOrderItemWithRelationsRDTO:
        """
        Получение и трансформация данных.

        Returns:
            ProductOrderItemWithRelationsRDTO: Элемент заказа с relationships
        """
        item = await self.product_order_item_repository.get(
            id=self.item_id,
            options=self.product_order_item_repository.default_relationships(),
            include_deleted_filter=self.include_deleted
        )

        return ProductOrderItemWithRelationsRDTO.model_validate(item)