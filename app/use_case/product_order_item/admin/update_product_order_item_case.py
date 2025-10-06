from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemCDTO, ProductOrderItemWithRelationsRDTO
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateProductOrderItemCase(BaseUseCase[ProductOrderItemWithRelationsRDTO]):
    """
    Use Case для обновления элемента заказа (админ).

    Основная функциональность:
    - Обновляет существующий элемент заказа
    - Проверяет существование элемента
    - Возвращает обновленный элемент с relationships
    - Доступ только для администраторов

    Attributes:
        product_order_item_repository: Репозиторий для работы с элементами заказов
        item_id: ID элемента заказа для обновления
        dto: DTO с данными для обновления

    Returns:
        ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа с relationships

    Raises:
        AppExceptionResponse: При отсутствии элемента заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для обновления элемента заказа.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.item_id: int | None = None
        self.dto: ProductOrderItemCDTO | None = None
        self.model = None

    async def execute(
        self,
        item_id: int,
        dto: ProductOrderItemCDTO
    ) -> ProductOrderItemWithRelationsRDTO:
        """
        Основной метод выполнения обновления элемента заказа.

        Обновляет элемент заказа по ID с предоставленными данными.

        Args:
            item_id (int): ID элемента заказа для обновления
            dto (ProductOrderItemCDTO): DTO с данными для обновления

        Returns:
            ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа с relationships

        Raises:
            AppExceptionResponse: При отсутствии элемента заказа
        """
        self.item_id = item_id
        self.dto = dto

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет существование элемента заказа и корректность данных.

        Raises:
            AppExceptionResponse: При отсутствии элемента заказа или некорректных данных
        """
        if not self.item_id or not self.dto:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        # Получаем элемент заказа для проверки существования
        self.model = await self.product_order_item_repository.get(
            id=self.item_id,
            include_deleted_filter=True
        )

        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_not_found")
            )

    async def transform(self) -> ProductOrderItemWithRelationsRDTO:
        """
        Обновление и трансформация данных.

        Returns:
            ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа с relationships
        """
        # Обновляем элемент заказа
        updated_item = await self.product_order_item_repository.update(
            obj=self.model,
            dto=self.dto
        )

        # Получаем обновленный элемент с relationships
        updated_item_with_relations = await self.product_order_item_repository.get(
            id=updated_item.id,
            options=self.product_order_item_repository.default_relationships(),
            include_deleted_filter=True
        )

        return ProductOrderItemWithRelationsRDTO.model_validate(updated_item_with_relations)