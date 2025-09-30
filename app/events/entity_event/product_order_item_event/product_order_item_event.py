import random
from datetime import datetime
from sqlalchemy import insert, select, func, update, inspect
from sqlalchemy.orm import Mapper

from app.entities import (
    ProductOrderItemEntity,
    ProductOrderItemHistoryEntity,
    ProductOrderItemVerificationCodeEntity,
    ProductOrderEntity,
)
from app.events.entity_event.entity_event_handler import EntityEventHandler
from app.shared.db_value_constants import DbValueConstants


class ProductOrderItemEventHandler(EntityEventHandler):
    """
    Обработчик событий для ProductOrderItemEntity.

    Основная функциональность:
    - При создании (insert) элемента заказа автоматически создает запись истории и код верификации
    - При обновлении (update) элемента заказа пересчитывает total_price в ProductOrderEntity
    - При удалении (delete) элемента заказа пересчитывает total_price в ProductOrderEntity
    """

    @staticmethod
    def after_insert(mapper: Mapper, connection, target):
        """
        Обработчик после создания ProductOrderItemEntity.

        Создает:
        1. ProductOrderItemHistoryEntity - запись истории создания элемента
        2. ProductOrderItemVerificationCodeEntity - код верификации для элемента
        """
        ProductOrderItemEventHandler._create_history_record(connection, target)
        ProductOrderItemEventHandler._create_verification_code(connection, target)
        ProductOrderItemEventHandler._recalculate_order_total(connection, target)

    @staticmethod
    def after_update(mapper: Mapper, connection, target):
        """
        Обработчик после обновления ProductOrderItemEntity.

        Пересчитывает total_price в ProductOrderEntity.
        Если status_id изменился, создает новую запись истории.

        Особая логика:
        1. При переходе в статус 2 (Оплачен, ожидает подтверждения) создается две записи истории:
           - Для статуса 1 (Создан, ожидает оплаты) с is_passed=True и passed_at
           - Для статуса 2 (Оплачен, ожидает подтверждения)
        2. При отмене элемента заказа (переход в статус 7) пересчитывает total_price
           и если он стал 0, меняет статус ProductOrder на 4 (Отменен, ожидает возврата)
        """
        # Проверяем, изменился ли status_id через inspect
        state = inspect(target)
        history = state.attrs.status_id.history

        # Если есть изменения в status_id
        if history.has_changes():
            old_status = history.deleted[0] if history.deleted else None
            new_status = target.status_id

            # Особая логика для перехода на статус 2 (оплачен)
            if (old_status == DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID and
                new_status == DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID):
                # Создаем запись для статуса 1 с is_passed=True (оплата прошла успешно)
                ProductOrderItemEventHandler._create_payment_history(connection, target)

            # Создаем обычную запись истории для нового статуса
            ProductOrderItemEventHandler._create_status_change_history(connection, target)

        # Пересчитываем total_price заказа
        ProductOrderItemEventHandler._recalculate_order_total(connection, target)

        # Проверяем, нужно ли изменить статус заказа на "Отменен, ожидает возврата"
        ProductOrderItemEventHandler._check_and_update_order_status(connection, target)

    @staticmethod
    def after_delete(mapper: Mapper, connection, target):
        """
        Обработчик после удаления ProductOrderItemEntity.

        Пересчитывает total_price в ProductOrderEntity.
        Проверяет, нужно ли изменить статус заказа на "Отменен, ожидает возврата".
        """
        ProductOrderItemEventHandler._recalculate_order_total(connection, target)
        ProductOrderItemEventHandler._check_and_update_order_status(connection, target)

    @staticmethod
    def _create_history_record(connection, target):
        """
        Создает запись истории для нового элемента заказа.

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, который был создан
        """
        connection.execute(
            insert(ProductOrderItemHistoryEntity).values(
                order_item_id=target.id,
                status_id=target.status_id,
                responsible_user_id=None,
                message_ru="Товар добавлен в заказ",
                message_kk="Тауар тапсырысқа қосылды",
                message_en="Item added to order",
                is_passed=None,
                cancel_reason=None,
                taken_at=None,
                passed_at=None,
            )
        )

    @staticmethod
    def _create_status_change_history(connection, target):
        """
        Создает запись истории при изменении статуса элемента заказа.

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, у которого изменился статус
        """
        connection.execute(
            insert(ProductOrderItemHistoryEntity).values(
                order_item_id=target.id,
                status_id=target.status_id,
                responsible_user_id=None,
                message_ru="Статус товара изменен",
                message_kk="Тауар күйі өзгертілді",
                message_en="Item status changed",
                is_passed=None,
                cancel_reason=target.cancel_reason if target.is_canceled else None,
                taken_at=None,
                passed_at=None,
            )
        )

    @staticmethod
    def _create_payment_history(connection, target):
        """
        Создает запись истории для статуса 1 (Создан, ожидает оплаты) при успешной оплате.
        Запись создается с is_passed=True и passed_at, показывая что оплата прошла успешно.

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, который был оплачен
        """
        now = datetime.now()
        connection.execute(
            insert(ProductOrderItemHistoryEntity).values(
                order_item_id=target.id,
                status_id=DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID,  # Статус 1
                responsible_user_id=None,
                message_ru="Заказ успешно оплачен",
                message_kk="Тапсырыс сәтті төленді",
                message_en="Order successfully paid",
                is_passed=True,  # Оплата прошла успешно
                cancel_reason=None,
                taken_at=now,  # Взято в обработку автоматически
                passed_at=now,  # И сразу пройдено
            )
        )

    @staticmethod
    def _create_verification_code(connection, target):
        """
        Создает код верификации для нового элемента заказа.
        Генерирует 4-значный числовой код.

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, который был создан
        """
        # Генерируем 4-значный код верификации
        verification_code = str(random.randint(1000, 9999))

        connection.execute(
            insert(ProductOrderItemVerificationCodeEntity).values(
                order_item_id=target.id,
                responsible_user_id=None,
                code=verification_code,
                is_active=True,
            )
        )

    @staticmethod
    def _recalculate_order_total(connection, target):
        """
        Пересчитывает total_price в ProductOrderEntity на основе суммы всех ProductOrderItemEntity.

        Суммируются только элементы, которые НЕ в статусе "Отменен, ожидает возврата" (7)
        и НЕ удалены (deleted_at is None).

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, который был изменен
        """
        connection.execute(
            update(ProductOrderEntity)
            .where(ProductOrderEntity.id == target.order_id)
            .values(
                total_price=(
                    select(func.coalesce(func.sum(ProductOrderItemEntity.total_price), 0))
                    .where(
                        (ProductOrderItemEntity.order_id == target.order_id) &
                        (ProductOrderItemEntity.deleted_at.is_(None)) &
                        (ProductOrderItemEntity.status_id != DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID)
                    )
                    .scalar_subquery()
                )
            )
        )

    @staticmethod
    def _check_and_update_order_status(connection, target):
        """
        Проверяет состояние заказа и обновляет статус в зависимости от элементов:
        - Если не осталось ни одного активного элемента (все удалены) -> статус 3 (Отменен)
        - Если остались элементы, но все отменены (total_price = 0) -> статус 4 (Отменен, ожидает возврата)

        Args:
            connection: SQLAlchemy connection для выполнения запросов
            target: Экземпляр ProductOrderItemEntity, который был изменен
        """
        # Проверяем, сколько элементов осталось в заказе (не удаленных)
        items_count_query = select(func.count(ProductOrderItemEntity.id)).where(
            (ProductOrderItemEntity.order_id == target.order_id) &
            (ProductOrderItemEntity.deleted_at.is_(None))
        )
        items_count_result = connection.execute(items_count_query)
        items_count = items_count_result.scalar()

        # Если не осталось ни одного элемента -> статус 3 (Отменен)
        if items_count == 0:
            connection.execute(
                update(ProductOrderEntity)
                .where(ProductOrderEntity.id == target.order_id)
                .values(
                    status_id=DbValueConstants.ProductOrderStatusCancelledID,  # Статус 3
                    is_canceled=True,
                    is_active=False,
                )
            )
            return

        # Получаем текущий total_price заказа
        total_price_query = select(ProductOrderEntity.total_price).where(
            ProductOrderEntity.id == target.order_id
        )
        total_price_result = connection.execute(total_price_query)
        total_price = total_price_result.scalar()

        # Если остались элементы, но total_price = 0 (все отменены) -> статус 4 (Отменен, ожидает возврата)
        if total_price is not None and total_price == 0:
            connection.execute(
                update(ProductOrderEntity)
                .where(ProductOrderEntity.id == target.order_id)
                .values(
                    status_id=DbValueConstants.ProductOrderStatusCancelledAwaitingRefundID,  # Статус 4
                    is_canceled=True,
                    is_active=False,
                )
            )

    @staticmethod
    def before_insert(mapper: Mapper, connection, target):
        """Обработчик перед вставкой - не используется в текущей реализации"""
        pass

    @staticmethod
    def before_update(mapper: Mapper, connection, target):
        """Обработчик перед обновлением - не используется в текущей реализации"""
        pass

    @staticmethod
    def before_delete(mapper: Mapper, connection, target):
        """Обработчик перед удалением - не используется в текущей реализации"""
        pass