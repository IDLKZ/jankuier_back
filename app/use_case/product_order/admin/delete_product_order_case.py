from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteProductOrderCase(BaseUseCase[bool]):
    """
    Use Case для удаления заказа (админ).

    Основная функциональность:
    - Удаляет заказ (мягкое или жесткое удаление)
    - Проверяет существование заказа
    - Поддерживает force_delete для полного удаления
    - Доступ только для администраторов

    Attributes:
        product_order_repository: Репозиторий для работы с заказами
        order_id: ID заказа для удаления
        force_delete: Флаг для полного удаления

    Returns:
        bool: True при успешном удалении

    Raises:
        AppExceptionResponse: При отсутствии заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для удаления заказа.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_repository = ProductOrderRepository(db)
        self.order_id: int | None = None
        self.force_delete: bool = False

    async def execute(
        self,
        order_id: int,
        force_delete: bool = False
    ) -> bool:
        """
        Основной метод выполнения удаления заказа.

        Удаляет заказ по ID с возможностью полного удаления.

        Args:
            order_id (int): ID заказа для удаления
            force_delete (bool, optional): Флаг полного удаления. По умолчанию False.

        Returns:
            bool: True при успешном удалении

        Raises:
            AppExceptionResponse: При отсутствии заказа
        """
        self.order_id = order_id
        self.force_delete = force_delete

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

        # Проверяем существование заказа
        order = await self.product_order_repository.get(
            id=self.order_id,
            include_deleted_filter=True
        )

        if not order:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_not_found")
            )

    async def transform(self) -> bool:
        """
        Удаление данных.

        Returns:
            bool: True при успешном удалении
        """
        try:
            await self.product_order_repository.delete(
                id=self.order_id,
                force_delete=self.force_delete
            )
            return True
        except Exception:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("delete_error")
            )