from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteProductOrderItemCase(BaseUseCase[bool]):
    """
    Use Case для удаления элемента заказа (админ).

    Основная функциональность:
    - Удаляет элемент заказа (мягкое или жесткое удаление)
    - Проверяет существование элемента
    - Поддерживает force_delete для полного удаления
    - Доступ только для администраторов

    Attributes:
        product_order_item_repository: Репозиторий для работы с элементами заказов
        item_id: ID элемента заказа для удаления
        force_delete: Флаг для полного удаления

    Returns:
        bool: True при успешном удалении

    Raises:
        AppExceptionResponse: При отсутствии элемента заказа
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case для удаления элемента заказа.

        Args:
            db: Активная сессия базы данных для выполнения операций
        """
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.item_id: int | None = None
        self.force_delete: bool = False

    async def execute(
        self,
        item_id: int,
        force_delete: bool = False
    ) -> bool:
        """
        Основной метод выполнения удаления элемента заказа.

        Удаляет элемент заказа по ID с возможностью полного удаления.

        Args:
            item_id (int): ID элемента заказа для удаления
            force_delete (bool, optional): Флаг полного удаления. По умолчанию False.

        Returns:
            bool: True при успешном удалении

        Raises:
            AppExceptionResponse: При отсутствии элемента заказа
        """
        self.item_id = item_id
        self.force_delete = force_delete

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

        # Проверяем существование элемента заказа
        item = await self.product_order_item_repository.get(
            id=self.item_id,
            include_deleted_filter=True
        )

        if not item:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("product_order_item_not_found")
            )

    async def transform(self) -> bool:
        """
        Удаление данных.

        Returns:
            bool: True при успешном удалении
        """
        try:
            await self.product_order_item_repository.delete(
                id=self.item_id,
                force_delete=self.force_delete
            )
            return True
        except Exception:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("delete_error")
            )