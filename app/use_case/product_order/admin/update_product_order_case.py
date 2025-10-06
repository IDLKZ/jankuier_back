from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order.product_order_dto import ProductOrderCDTO, ProductOrderWithRelationsRDTO
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateProductOrderCase(BaseUseCase[ProductOrderWithRelationsRDTO]):
    """
    Use Case для обновления заказа (админ).

    Основная функциональность:
    - Обновляет существующий заказ
    - Проверяет существование заказа
    - Возвращает обновленный заказ с relationships
    - Доступ только для администраторов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        order_id: ID заказа для обновления
        dto: DTO с данными для обновления

    Returns:
        ProductOrderWithRelationsRDTO: Обновленный заказ с relationships

    Raises:
        AppExceptionResponse: При отсутствии заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для обновления заказа.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.order_id: int | None = None
        self.dto: ProductOrderCDTO | None = None
        self.model = None

    async def execute(
        self,
        order_id: int,
        dto: ProductOrderCDTO
    ) -> ProductOrderWithRelationsRDTO:
        """
        Основной метод выполнения обновления заказа.

        Обновляет заказ по ID с предоставленными данными.

        Args:
            order_id (int): ID заказа для обновления
            dto (ProductOrderCDTO): DTO с данными для обновления

        Returns:
            ProductOrderWithRelationsRDTO: Обновленный заказ с relationships

        Raises:
            AppExceptionResponse: При отсутствии заказа
        """
        self.order_id = order_id
        self.dto = dto

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация входных данных.

        Проверяет существование заказа и корректность данных.

        Raises:
            AppExceptionResponse: При отсутствии заказа или некорректных данных
        """
        if not self.order_id or not self.dto:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_parameters")
            )

        # Получаем заказ для проверки существования
        self.model = await self.product_order_repository.get(
            id=self.order_id,
            include_deleted_filter=True
        )

        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_not_found")
            )

    async def transform(self) -> ProductOrderWithRelationsRDTO:
        """
        Обновление и трансформация данных.

        Returns:
            ProductOrderWithRelationsRDTO: Обновленный заказ с relationships
        """
        # Обновляем заказ
        updated_order = await self.product_order_repository.update(
            obj=self.model,
            dto=self.dto
        )

        # Получаем обновленный заказ с relationships
        updated_order_with_relations = await self.product_order_repository.get(
            id=updated_order.id,
            options=self.product_order_repository.default_relationships(),
            include_deleted_filter=True
        )

        return ProductOrderWithRelationsRDTO.model_validate(updated_order_with_relations)