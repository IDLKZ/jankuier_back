from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO, \
    ProductOrderItemCDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.product_order.product_order_repository import ProductOrderRepository
from app.adapters.repository.product_order_item.product_order_item_repository import ProductOrderItemRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderEntity, ProductOrderItemEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CancelOrderItemCase(BaseUseCase[Optional[ProductOrderItemWithRelationsRDTO]]):
    """
    Use case для отмены элемента заказа клиентом.

    Функциональность:
    - Если статус "Создан, ожидает оплаты" - удаляет элемент заказа (force delete)
    - Если статус "Оплачен, ожидает подтверждения" - меняет статус на "Отменен, ожидает возврата"
    - Автоматически пересчитывает total_price заказа через event handler
    - Валидирует принадлежность заказа текущему пользователю
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация use case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.product_order_repository = ProductOrderRepository(db)

        self.current_product_order: ProductOrderEntity | None = None
        self.current_product_order_item: ProductOrderItemEntity | None = None

        self.current_user: UserWithRelationsRDTO | None = None
        self.order_item_id: int | None = None
        self.cancel_reason: str | None = None

    async def execute(
        self,
        order_item_id: int,
        user: UserWithRelationsRDTO,
        cancel_reason: str | None = None
    ) -> Optional[ProductOrderItemWithRelationsRDTO]:
        """
        Выполнение отмены элемента заказа.

        Args:
            order_item_id: ID элемента заказа для отмены
            user: Текущий пользователь (клиент)
            cancel_reason: Причина отмены (опционально)

        Returns:
            ProductOrderItemWithRelationsRDTO если элемент был обновлен (статус изменен),
            None если элемент был удален

        Raises:
            AppExceptionResponse.bad_request: Если элемент не найден, не принадлежит пользователю,
                                             или уже отменен/завершен
        """
        self.current_user = user
        self.order_item_id = order_item_id
        self.cancel_reason = cancel_reason
        await self.validate()
        return await self.transform()


    async def validate(self) -> None:
        """
        Валидация возможности отмены элемента заказа.

        Проверяет:
        - Существование элемента заказа
        - Элемент не был удален (deleted_at is None)
        - Элемент принадлежит текущему пользователю
        - Статус элемента позволяет отмену (только "Создан" или "Оплачен, ожидает подтверждения")

        Raises:
            AppExceptionResponse.bad_request: При любой ошибке валидации
        """
        self.current_product_order_item = await self.product_order_item_repository.get(
            id=self.order_item_id,
            options=self.product_order_item_repository.default_relationships(),
            include_deleted_filter=True
        )
        if self.current_product_order_item is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_item_not_found"))

        # Проверяем, что заказ существует
        if self.current_product_order_item.order is None:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("product_order_not_found"))

        # Проверяем, что заказ принадлежит текущему пользователю
        if self.current_product_order_item.order.user_id != self.current_user.id:
            raise AppExceptionResponse.forbidden(message=i18n.gettext("access_denied"))

        # Проверяем, что элемент можно отменить (только определенные статусы)
        allowed_statuses = [
            DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,
            DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID,
        ]
        if self.current_product_order_item.status_id not in allowed_statuses:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_cannot_be_cancelled")
            )

        # Проверяем, что элемент еще не отменен
        if self.current_product_order_item.is_canceled:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_already_cancelled")
            )

        self.current_product_order = self.current_product_order_item.order


    async def transform(self) -> Optional[ProductOrderItemWithRelationsRDTO]:
        """
        Выполнение отмены элемента заказа в зависимости от статуса.

        Логика:
        - Статус "Создан, ожидает оплаты": удаляет элемент (force delete)
        - Статус "Оплачен, ожидает подтверждения": обновляет статус на "Отменен, ожидает возврата"

        При обновлении автоматически:
        - Устанавливается canceled_by_id
        - Сохраняется cancel_reason
        - Пересчитывается total_price заказа (через event handler)
        - Создается запись в ProductOrderItemHistory (через event handler)

        Returns:
            ProductOrderItemWithRelationsRDTO если элемент был обновлен,
            None если элемент был удален
        """
        # Случай 1: Заказ еще не оплачен - просто удаляем элемент
        if self.current_product_order_item.status_id == DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID:
            await self.product_order_item_repository.delete(
                id=self.current_product_order_item.id,
                force_delete=True
            )
            # После удаления event handler автоматически пересчитает total_price заказа
            return None

        # Случай 2: Заказ оплачен - меняем статус на "Отменен, ожидает возврата"
        if self.current_product_order_item.status_id == DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID:
            product_order_item_cdto = ProductOrderItemCDTO.from_orm(self.current_product_order_item)
            product_order_item_cdto.status_id = DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID
            product_order_item_cdto.is_active = False
            product_order_item_cdto.is_canceled = True
            product_order_item_cdto.canceled_by_id = self.current_user.id
            product_order_item_cdto.cancel_reason = self.cancel_reason

            self.current_product_order_item = await self.product_order_item_repository.update(
                obj=self.current_product_order_item,
                dto=product_order_item_cdto
            )
            # После обновления event handler автоматически:
            # 1. Создаст запись в ProductOrderItemHistory (т.к. status_id изменился)
            # 2. Пересчитает total_price заказа
            return ProductOrderItemWithRelationsRDTO.from_orm(self.current_product_order_item)

        # Этот код не должен выполниться благодаря валидации, но на всякий случай
        return None







