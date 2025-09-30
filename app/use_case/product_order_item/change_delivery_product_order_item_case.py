from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_order_item.product_order_item_dto import (
    ProductOrderItemWithRelationsRDTO,
    ChangeDeliveryProductOrderItemCDTO,
    ProductOrderItemCDTO,
)
from app.adapters.dto.product_order_item_history.product_order_item_history_dto import (
    ProductOrderItemHistoryCDTO,
)
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.repository.product_order_item.product_order_item_repository import (
    ProductOrderItemRepository,
)
from app.adapters.repository.product_order_item_history.product_order_item_history_repository import (
    ProductOrderItemHistoryRepository,
)
from app.adapters.repository.product_order_item_verification_code.product_order_item_verification_code_repository import (
    ProductOrderItemVerificationCodeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductOrderItemEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class ChangeDeliveryProductOrderItemCase(
    BaseUseCase[ProductOrderItemWithRelationsRDTO]
):
    """
    Use case для управления процессом доставки ProductOrderItem.

    Поддерживает два типа действий:
    1. "Принять в обработку" (is_passed=None):
       - Ответственное лицо берет задачу в работу
       - Заполняется responsible_user_id и taken_at
       - Создается запись в истории о взятии в работу

    2. "Принять решение" (is_passed=True/False):
       - is_passed=True: успешное прохождение этапа
         * Меняется status_id на новый статус
         * Заполняется passed_at
         * Для перехода 4->5 требуется verification_code
       - is_passed=False: отклонение/отмена
         * Меняется status_id на "Отменен, ожидает возврата" (7)
         * Заполняется cancel_reason
         * Заполняется passed_at

    Статусы обработки (начиная со статуса 2 "Оплачен, ожидает подтверждения"):
    - 2 -> 3: Принято в доставку
    - 3 -> 4: Доставлено, ожидает подтверждения получения
    - 4 -> 5: Успешно получено (на этапе статуса 4 требуется verification_code для перехода в 5)
    - 2/3/4 -> 7: Отменено, ожидает возврата (при is_passed=False)

    Все изменения автоматически:
    - Создают записи в ProductOrderItemHistory (через event handler при смене статуса)
    - Пересчитывают total_price заказа (через event handler)
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация use case.

        Args:
            db: Асинхронная сессия базы данных
        """
        self.db = db
        self.product_order_item_repository = ProductOrderItemRepository(db)
        self.history_repository = ProductOrderItemHistoryRepository(db)
        self.verification_code_repository = ProductOrderItemVerificationCodeRepository(db)

        # Состояние use case
        self.current_order_item: ProductOrderItemEntity | None = None
        self.current_user: UserWithRelationsRDTO | None = None
        self.order_item_id: int | None = None
        self.dto: ChangeDeliveryProductOrderItemCDTO | None = None
        self.last_history_record = None

    async def execute(
        self,
        order_item_id: int,
        user: UserWithRelationsRDTO,
        dto: ChangeDeliveryProductOrderItemCDTO,
    ) -> ProductOrderItemWithRelationsRDTO:
        """
        Выполнение изменения статуса доставки.

        Args:
            order_item_id: ID элемента заказа
            user: Текущий ответственный пользователь
            dto: DTO с данными для изменения статуса

        Returns:
            ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа со всеми связями

        Raises:
            AppExceptionResponse.bad_request: При ошибках валидации или неверном verification_code
            AppExceptionResponse.forbidden: При отсутствии прав доступа
        """
        self.order_item_id = order_item_id
        self.current_user = user
        self.dto = dto

        await self.validate()
        return await self.transform()

    async def validate(self) -> None:
        """
        Валидация возможности изменения статуса доставки.

        Проверяет:
        - Существование элемента заказа
        - Статус элемента >= 2 (начиная с "Оплачен, ожидает подтверждения")
        - Наличие последней записи в истории с заполненным responsible_user_id и taken_at
        - Корректность перехода статусов
        - Наличие verification_code для статуса "Успешно получен"
        - Наличие cancel_reason при is_passed=False

        Raises:
            AppExceptionResponse.bad_request: При любой ошибке валидации
        """
        # 1. Проверяем существование элемента заказа
        self.current_order_item = await self.product_order_item_repository.get(
            id=self.order_item_id,
            options=self.product_order_item_repository.default_relationships(),
            include_deleted_filter=True,
        )
        if self.current_order_item is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_not_found")
            )

        # 2. Проверяем, что элемент в статусе >= 2 (обработка начинается со статуса "Оплачен")
        if (
            self.current_order_item.status_id
            < DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID
        ):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_not_ready_for_processing")
            )

        # 3. Проверяем, что элемент не отменен
        if self.current_order_item.is_canceled:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_order_item_already_cancelled")
            )

        # 5. Логика валидации в зависимости от действия
        if self.dto.is_passed is None:
            # Действие: "Принять в обработку"
            # 4. Получаем последнюю запись истории для проверки взятия в работу
            self.last_history_record = await self._get_last_history_record(True)
            await self._validate_take_to_work()
        else:
            # Действие: "Принять решение"
            self.last_history_record = await self._get_last_history_record(False)
            await self._validate_make_decision()

    async def _validate_take_to_work(self) -> None:
        """
        Валидация действия "Принять в обработку".

        Проверяет, что предыдущий этап был завершен (passed_at заполнен)
        или это первое взятие в работу.
        """
        # Если есть последняя запись истории
        if self.last_history_record:
            # Проверяем, что предыдущий этап завершен (passed_at заполнен)
            if (self.last_history_record.passed_at is None
                    and self.last_history_record.status_id != DbValueConstants.ProductOrderItemStatusCreatedAwaitingPaymentID
            ):
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("previous_stage_not_completed") + f"{self.last_history_record.id}"
                )

    async def _validate_make_decision(self) -> None:
        """
        Валидация действия "Принять решение".

        Проверяет:
        - Задача взята в работу (taken_at заполнен)
        - Задача еще не завершена (passed_at пуст)
        - Корректность новых данных (статус, причина отмены, код верификации)
        """
        # 1. Проверяем, что задача взята в работу
        if not self.last_history_record or self.last_history_record.taken_at is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("order_item_not_taken_to_work")
            )

        # 2. Проверяем, что задача еще не завершена
        if self.last_history_record.passed_at is not None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("order_item_already_processed" + f"{self.last_history_record.id}")
            )

        # 3. Валидация в зависимости от результата
        if self.dto.is_passed:
            # Успешное прохождение - проверяем новый статус
            await self._validate_success_decision()
        else:
            # Отклонение - проверяем причину отмены
            await self._validate_cancel_decision()

    async def _validate_success_decision(self) -> None:
        """
        Валидация успешного прохождения этапа (is_passed=True).

        Проверяет:
        - Указан новый статус
        - Новый статус корректен для текущего статуса
        - Для перехода из статуса 4 в статус 5 указан и корректен verification_code
        """
        if not self.dto.new_status_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("new_status_required")
            )

        # Проверяем корректность перехода статуса
        valid_transitions = {
            DbValueConstants.ProductOrderItemStatusPaidAwaitingConfirmationID: [
                DbValueConstants.ProductOrderItemStatusInDeliveryID  # 2 -> 3
            ],
            DbValueConstants.ProductOrderItemStatusInDeliveryID: [
                DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID  # 3 -> 4
            ],
            DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID: [
                DbValueConstants.ProductOrderItemStatusSuccessfullyReceivedID  # 4 -> 5
            ],
        }

        current_status = self.current_order_item.status_id
        if current_status not in valid_transitions:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_current_status")
            )

        if self.dto.new_status_id not in valid_transitions[current_status]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_status_transition")
            )

        # Для перехода из статуса "Ожидает подтверждения доставки" (4) в "Успешно получен" (5)
        # требуется код верификации
        if (
            current_status
            == DbValueConstants.ProductOrderItemStatusAwaitingDeliveryConfirmationID
            and self.dto.new_status_id
            == DbValueConstants.ProductOrderItemStatusSuccessfullyReceivedID
        ):
            if not self.dto.verification_code:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("verification_code_required")
                )

            # Проверяем корректность кода верификации
            await self._validate_verification_code()

    async def _validate_cancel_decision(self) -> None:
        """
        Валидация отклонения/отмены (is_passed=False).

        Проверяет наличие причины отмены.
        """
        if not self.dto.cancel_reason:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cancel_reason_required")
            )

    async def _validate_verification_code(self) -> None:
        """
        Проверка корректности кода верификации.

        Загружает код верификации из БД через repository и сравнивает с введенным.

        Raises:
            AppExceptionResponse.bad_request: Если код неверен или не найден
        """
        # Получаем активный код верификации для данного элемента заказа
        verification_code_entity = await self.verification_code_repository.get_first_with_filters(
            filters=[
                self.verification_code_repository.model.order_item_id == self.order_item_id,
                self.verification_code_repository.model.is_active == True,
            ]
        )

        if not verification_code_entity:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("verification_code_not_found")
            )

        # Сравниваем коды (без учета регистра)
        if (
            verification_code_entity.code.upper()
            != self.dto.verification_code.upper()
        ):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("verification_code_invalid")
            )

    async def transform(self) -> ProductOrderItemWithRelationsRDTO:
        """
        Выполнение изменения статуса доставки.

        В зависимости от is_passed:
        - None: создает запись истории с taken_at
        - True/False: обновляет запись истории с passed_at и меняет статус элемента

        Returns:
            ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа
        """
        if self.dto.is_passed is None:
            # Действие: "Принять в обработку"
            await self._take_to_work()
        else:
            # Действие: "Принять решение"
            await self._make_decision()

        # Загружаем обновленный элемент заказа со всеми связями
        self.current_order_item = await self.product_order_item_repository.get(
            id=self.order_item_id,
            options=self.product_order_item_repository.default_relationships(),
        )

        return ProductOrderItemWithRelationsRDTO.from_orm(self.current_order_item)

    async def _take_to_work(self) -> None:
        """
        Выполнение действия "Принять в обработку".

        Проверяет существование активной записи истории для текущего статуса:
        - Если запись существует: обновляет только responsible_user_id
        - Если записи нет: создает новую запись с taken_at и responsible_user_id
        """
        # Проверяем, есть ли уже активная запись истории для текущего статуса
        existing_history = await self.history_repository.get_first_with_filters(
            filters=[
                self.history_repository.model.order_item_id == self.order_item_id,
                self.history_repository.model.status_id == self.current_order_item.status_id,
                self.history_repository.model.passed_at.is_(None),  # Запись еще не завершена
            ],
            order_by="created_at",
            order_direction="desc",
        )

        if existing_history:
            # Если запись уже есть, только обновляем responsible_user_id
            update_dto = ProductOrderItemHistoryCDTO.from_orm(existing_history)
            update_dto.responsible_user_id = self.current_user.id
            update_dto.taken_at=datetime.now()

            # Обновляем сообщения, если они указаны в DTO
            if self.dto.message_ru:
                update_dto.message_ru = self.dto.message_ru
            if self.dto.message_kk:
                update_dto.message_kk = self.dto.message_kk
            if self.dto.message_en:
                update_dto.message_en = self.dto.message_en

            await self.history_repository.update(obj=existing_history, dto=update_dto)
        else:
            # Если записи нет, создаем новую
            history_dto = ProductOrderItemHistoryCDTO(
                order_item_id=self.order_item_id,
                status_id=self.current_order_item.status_id,
                responsible_user_id=self.current_user.id,
                message_ru=self.dto.message_ru or "Принято в обработку",
                message_kk=self.dto.message_kk or "Өңдеуге қабылданды",
                message_en=self.dto.message_en or "Taken to processing",
                is_passed=None,
                cancel_reason=None,
                taken_at=datetime.now(),
                passed_at=None,
            )

            await self.history_repository.create(self.history_repository.model(**history_dto.dict()))

    async def _make_decision(self) -> None:
        """
        Выполнение действия "Принять решение".

        Обновляет последнюю запись истории с passed_at и результатом (is_passed).
        Меняет статус ProductOrderItem в зависимости от is_passed.

        При is_passed=True:
        - Меняет статус на новый (из DTO)
        - Заполняет passed_at

        При is_passed=False:
        - Меняет статус на "Отменен, ожидает возврата" (7)
        - Заполняет cancel_reason и passed_at
        """
        # 1. Обновляем запись истории
        await self._update_history_record()

        # 2. Обновляем статус элемента заказа
        if self.dto.is_passed:
            # Успешное прохождение - меняем статус на новый
            await self._update_order_item_status_success()
        else:
            # Отклонение - меняем статус на "Отменен, ожидает возврата"
            await self._update_order_item_status_cancel()

    async def _update_history_record(self) -> None:
        """
        Обновление последней записи истории с результатом принятия решения.

        Заполняет:
        - is_passed (результат)
        - passed_at (время завершения)
        - cancel_reason (если отклонено)
        - сообщения (если указаны в DTO)
        """
        # Создаем DTO для обновления
        update_dto = ProductOrderItemHistoryCDTO.from_orm(self.last_history_record)
        update_dto.is_passed = self.dto.is_passed
        update_dto.passed_at = datetime.now()
        update_dto.cancel_reason = self.dto.cancel_reason if not self.dto.is_passed else None

        # Обновляем сообщения, если они указаны
        if self.dto.message_ru:
            update_dto.message_ru = self.dto.message_ru
        if self.dto.message_kk:
            update_dto.message_kk = self.dto.message_kk
        if self.dto.message_en:
            update_dto.message_en = self.dto.message_en

        # Обновляем запись
        await self.history_repository.update(
            obj=self.last_history_record, dto=update_dto
        )

    async def _update_order_item_status_success(self) -> None:
        """
        Обновление статуса элемента заказа при успешном прохождении (is_passed=True).

        Меняет status_id на новый статус из DTO.
        Event handler автоматически:
        - Создаст новую запись в истории (т.к. status_id изменился)
        - Пересчитает total_price заказа
        """
        order_item_dto = ProductOrderItemCDTO.from_orm(self.current_order_item)
        order_item_dto.status_id = self.dto.new_status_id

        self.current_order_item = await self.product_order_item_repository.update(
            obj=self.current_order_item, dto=order_item_dto
        )

    async def _update_order_item_status_cancel(self) -> None:
        """
        Обновление статуса элемента заказа при отклонении (is_passed=False).

        Меняет status_id на "Отменен, ожидает возврата" (7).
        Устанавливает флаги is_canceled=True, is_active=False.
        Сохраняет cancel_reason и canceled_by_id.

        Event handler автоматически:
        - Создаст новую запись в истории (т.к. status_id изменился)
        - Пересчитает total_price заказа
        """
        order_item_dto = ProductOrderItemCDTO.from_orm(self.current_order_item)
        order_item_dto.status_id = (
            DbValueConstants.ProductOrderItemStatusCancelledAwaitingRefundID
        )
        order_item_dto.is_canceled = True
        order_item_dto.is_active = False
        order_item_dto.canceled_by_id = self.current_user.id
        order_item_dto.cancel_reason = self.dto.cancel_reason

        self.current_order_item = await self.product_order_item_repository.update(
            obj=self.current_order_item, dto=order_item_dto
        )

    async def _get_last_history_record(self, check_the_same: bool = False):
        """
        Получение последней записи истории для элемента заказа через repository.

        Args:
            check_the_same: Если True, получает запись с тем же status_id (для текущего этапа)
                           Если False, получает запись с другим status_id (для предыдущего этапа)

        Returns:
            ProductOrderItemHistoryEntity | None: Последняя запись истории или None
        """
        # Получаем все записи истории для данного элемента заказа, отсортированные по дате создания
        filters = [
            self.history_repository.model.order_item_id == self.order_item_id,
        ]

        if check_the_same:
            # Получаем запись с тем же статусом (текущий этап)
            filters.append(self.history_repository.model.status_id != self.current_order_item.status_id)
        history_records = await self.history_repository.get_with_filters(
            filters=filters,
            order_by="id",
            order_direction="desc",
        )

        # Возвращаем первую запись (самую последнюю) или None
        return history_records[0] if history_records else None