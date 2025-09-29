from sqlalchemy import update
from sqlalchemy.orm import Mapper

from app.entities import ProductOrderEntity, ProductOrderItemEntity
from app.events.entity_event.entity_event_handler import EntityEventHandler
from app.shared.db_value_constants import DbValueConstants


class ProductOrderEventHandler(EntityEventHandler):
    """
    Обработчик событий для ProductOrderEntity.

    Основная функциональность:
    - При изменении статуса заказа автоматически обновляет статусы всех элементов заказа
    - Реализует соответствие статусов согласно бизнес-логике:
      * ProductOrder.status_id 2 -> ProductOrderItem.status_id 2
      * ProductOrder.status_id 3 -> ProductOrderItem.status_id 6
      * ProductOrder.status_id 4 -> ProductOrderItem.status_id 7
      * ProductOrder.status_id 5 -> ProductOrderItem.status_id 8
    """

    @staticmethod
    def after_update(mapper: Mapper, connection, target):
        """
        Обработчик события после обновления ProductOrderEntity.

        Проверяет изменение status_id и обновляет соответствующие статусы
        у всех ProductOrderItemEntity связанных с данным заказом.
        """
        ProductOrderEventHandler._sync_order_item_statuses(connection, target)

    @staticmethod
    def _sync_order_item_statuses(connection, target):
        """
        Синхронизирует статусы элементов заказа с статусом основного заказа.

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderEntity, который был обновлен
        """
        # Получаем текущий статус заказа
        order_status_id = target.status_id

        # Определяем соответствующий статус для элементов заказа
        item_status_mapping = {
            DbValueConstants.ProductOrderStatusPaidID: DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID,  # 2 -> 2
            DbValueConstants.ProductOrderStatusCancelledID: DbValueConstants.ProductOrderItemStatusCancelledID,  # 3 -> 6
            DbValueConstants.ProductOrderStatusCancelledAwaitingRefundID: DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID,  # 4 -> 7
            DbValueConstants.ProductOrderStatusCancelledRefundedID: DbValueConstants.ProductOrderItemStatusCancelledRefundedID,  # 5 -> 8
        }

        # Если статус заказа соответствует одному из отслеживаемых
        if order_status_id in item_status_mapping:
            new_item_status_id = item_status_mapping[order_status_id]

            # Обновляем статус всех элементов заказа
            connection.execute(
                update(ProductOrderItemEntity)
                .where(
                    (ProductOrderItemEntity.order_id == target.id) &
                    (ProductOrderItemEntity.deleted_at.is_(None))
                )
                .values(status_id=new_item_status_id)
            )

    @staticmethod
    def before_insert(mapper: Mapper, connection, target):
        """Обработчик перед вставкой - не используется в текущей реализации"""
        pass

    @staticmethod
    def after_insert(mapper: Mapper, connection, target):
        """Обработчик после вставки - не используется в текущей реализации"""
        pass

    @staticmethod
    def before_update(mapper: Mapper, connection, target):
        """Обработчик перед обновлением - не используется в текущей реализации"""
        pass

    @staticmethod
    def before_delete(mapper: Mapper, connection, target):
        """Обработчик перед удалением - не используется в текущей реализации"""
        pass

    @staticmethod
    def after_delete(mapper: Mapper, connection, target):
        """Обработчик после удаления - не используется в текущей реализации"""
        pass