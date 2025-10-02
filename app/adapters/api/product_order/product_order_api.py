import traceback

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.adapters.dto.alatau.alatau_after_payment_dto import AlatauBackrefGetDTO
from app.adapters.dto.pagination_dto import PaginationProductOrderWithRelationsRDTO, PaginationProductOrderItemWithRelationsRDTO
from app.adapters.dto.product_order.full_product_order_dto import FullProductOrderRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemWithRelationsRDTO
from app.adapters.dto.product_order_response.product_order_response_dto import ProductOrderWithPaymentTransactionResponseDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.adapters.filters.product_order.product_order_pagination_filter import ProductOrderPaginationFilter
from app.adapters.filters.product_order_item.product_order_item_pagination_filter import ProductOrderItemPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.adapters.dto.product_order_response.product_order_response_dto import ProductOrderResponseDTO
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.middleware.role_middleware import check_client
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order.client.accept_payment_product_order_case import AcceptPaymentProductOrderCase
from app.use_case.product_order.client.cancel_or_delete_order_case import CancelOrDeleteOrderCase
from app.use_case.product_order.client.create_product_order_case import CreateProductOrderCase
from app.use_case.product_order.client.get_my_order_by_id_case import GetMyOrderByIdCase
from app.use_case.product_order.client.my_order_case import MyOrderCase
from app.use_case.product_order.client.my_order_item_case import MyOrderItemCase
from app.use_case.product_order.client.recreate_product_order_by_id_case import RecreateProductOrderByIdCase
from app.use_case.product_order_item.client.cancel_order_item_case import CancelOrderItemCase


class ProductOrderApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "/create-order-from-cart",
            response_model=ProductOrderResponseDTO,
            summary="Создание заказа из корзины",
            description="Создает заказ на основе содержимого корзины пользователя с интеграцией платежной системы",
        )(self.create_order)

        self.router.post(
            "/recreate-payment/{id}",
            response_model=ProductOrderResponseDTO,
            summary="Пересоздание платежной транзакции для заказа",
            description="Создает новую платежную транзакцию для существующего заказа, деактивируя старые",
        )(self.recreate_payment)

        self.router.get(
            "/client-my-orders",
            response_model=PaginationProductOrderWithRelationsRDTO,
            summary="Мои заказы (пагинированный список)",
            description="Получение пагинированного списка заказов текущего пользователя с возможностью фильтрации и сортировки",
        )(self.get_my_orders)

        self.router.get(
            "/client-my-order/{id}",
            response_model=FullProductOrderRDTO,
            summary="Получить мой заказ по ID",
            description="Получение конкретного заказа пользователя по его идентификатору",
        )(self.get_my_order_by_id)

        self.router.get(
            "/client-my-order-items/{id}",
            response_model=PaginationProductOrderItemWithRelationsRDTO,
            summary="Элементы моего заказа",
            description="Получение пагинированного списка элементов конкретного заказа пользователя",
        )(self.get_my_order_items)

        self.router.delete(
            "/client-cancel-or-delete-order/{id}",
            response_model=bool,
            summary="Отмена или удаление заказа",
            description="Отменяет заказ (при статусе ожидания оплаты) или помечает на возврат (при оплаченном статусе), либо удаляет заказ",
        )(self.cancel_or_delete_order)

        self.router.get(
            "/accept-payment",
            response_model=ProductOrderWithPaymentTransactionResponseDTO,
            summary="Подтверждение платежа заказа",
            description="Обрабатывает GET callback от платежной системы Alatau Pay для подтверждения оплаты заказа товаров",
        )(self.accept_payment)

        self.router.post(
            "/client-cancel-order-item/{order_item_id}",
            response_model=ProductOrderItemWithRelationsRDTO | None,
            summary="Отмена элемента заказа клиентом",
            description="Позволяет клиенту отменить конкретный элемент своего заказа. Если заказ не оплачен - удаляет элемент, если оплачен - меняет статус на 'Ожидает возврата'",
        )(self.cancel_order_item)

    async def create_order(
        self,
        phone: Optional[str] = Form(None, description="Телефон для заказа (опционально)"),
        email: Optional[str] = Form(None, description="Email для заказа (опционально)"),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderResponseDTO:
        try:
            return await CreateProductOrderCase(db).execute(user=user, phone=phone, email=email)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details22": str(exc)},
                is_custom=True,
            ) from exc

    async def recreate_payment(
        self,
        id: RoutePathConstants.IDPath,
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderResponseDTO:
        """
        Пересоздает платежную транзакцию для существующего заказа.

        Args:
            id: ID заказа для пересоздания платежной транзакции
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            ProductOrderResponseDTO: Ответ с новой платежной транзакцией

        Raises:
            HTTPException: При ошибках валидации или отсутствии прав доступа
        """
        try:
            return await RecreateProductOrderByIdCase(db).execute(id=id, user=user)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_my_orders(
        self,
        filter_obj: ProductOrderPaginationFilter = Depends(),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductOrderWithRelationsRDTO:
        """
        Получение пагинированного списка заказов текущего пользователя.

        Args:
            filter_obj: Объект фильтрации и пагинации заказов
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            PaginationProductOrderWithRelationsRDTO: Пагинированный список заказов пользователя

        Raises:
            HTTPException: При ошибках валидации или внутренних ошибках
        """
        try:
            return await MyOrderCase(db).execute(user=user, filter_obj=filter_obj)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_my_order_by_id(
        self,
        id: RoutePathConstants.IDPath,
        include_deleted: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> FullProductOrderRDTO:
        """
        Получение конкретного заказа пользователя по ID.

        Args:
            id: ID заказа для получения
            include_deleted: Включать удаленные записи
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с полными relationships

        Raises:
            HTTPException: При ошибках валидации, отсутствии прав доступа или не найден заказ
        """
        try:
            return await GetMyOrderByIdCase(db).execute(
                user=user, order_id=id, include_deleted=include_deleted or False
            )
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_my_order_items(
        self,
        id: RoutePathConstants.IDPath,
        filter_obj: ProductOrderItemPaginationFilter = Depends(),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Получение пагинированного списка элементов конкретного заказа пользователя.

        Args:
            id: ID заказа для получения элементов
            filter_obj: Объект фильтрации и пагинации элементов заказа
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            PaginationProductOrderItemWithRelationsRDTO: Пагинированный список элементов заказа

        Raises:
            HTTPException: При ошибках валидации, отсутствии прав доступа или не найден заказ
        """
        try:
            return await MyOrderItemCase(db).execute(
                user=user, order_id=id, filter_obj=filter_obj
            )
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def cancel_or_delete_order(
        self,
        id: RoutePathConstants.IDPath,
        is_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Отменяет или удаляет заказ пользователя.

        Логика работы:
        - Если заказ в статусе "Ожидает оплаты" - отменяет заказ
        - Если заказ оплачен - помечает на возврат средств
        - При is_delete=True - полностью удаляет заказ из системы

        Args:
            id: ID заказа для отмены/удаления
            is_delete: Флаг для полного удаления заказа (по умолчанию False - отмена)
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            bool: True при успешной операции, False при ошибке

        Raises:
            HTTPException: При ошибках валидации, отсутствии прав доступа или некорректном статусе заказа
        """
        try:
            return await CancelOrDeleteOrderCase(db).execute(
                id=id, user=user, is_delete=is_delete or False
            )
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def accept_payment(
        self,
        dto: AlatauBackrefGetDTO = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderWithPaymentTransactionResponseDTO:
        """
        Подтверждение платежа заказа товаров (GET callback).

        Обрабатывает GET callback от платежной системы Alatau Pay для подтверждения
        оплаты заказа товаров. Получает данные через query parameters, валидирует
        цифровую подпись, обновляет статус заказа и синхронизирует данные платежной транзакции.

        Args:
            dto: DTO с данными callback'а от Alatau Pay (из query parameters)
            db: Сессия базы данных

        Returns:
            ProductOrderWithPaymentTransactionResponseDTO: Полная информация о заказе,
            элементах заказа и платежной транзакции

        Raises:
            HTTPException: При невалидной подписи, отсутствии транзакции или заказа

        Notes:
            - GET эндпоинт для callback'ов от платежной системы
            - Доступен без аутентификации (Common role)
            - Данные передаются через query parameters
            - Автоматически обновляет статусы элементов заказа через события

        Example URL:
            GET /api/product-order/accept-payment?order=12345&res_code=0&amount=1000&currency=KZT&sign=abc123...
        """
        try:
            return await AcceptPaymentProductOrderCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def cancel_order_item(
        self,
        order_item_id: RoutePathConstants.IDPath,
        cancel_reason: Optional[str] = Form(None, description="Причина отмены элемента заказа (опционально)"),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemWithRelationsRDTO | None:
        """
        Отмена элемента заказа клиентом.

        Позволяет клиенту отменить конкретный элемент своего заказа:
        - Если статус "Создан, ожидает оплаты" - удаляет элемент заказа
        - Если статус "Оплачен, ожидает подтверждения" - меняет статус на "Отменен, ожидает возврата"

        Автоматически пересчитывает total_price заказа через event handler.

        Args:
            order_item_id: ID элемента заказа для отмены
            cancel_reason: Причина отмены (опционально)
            user: Текущий пользователь (автоматически извлекается из токена)
            db: Сессия базы данных

        Returns:
            ProductOrderItemWithRelationsRDTO если элемент был обновлен (статус изменен),
            None если элемент был удален

        Raises:
            HTTPException: При ошибках валидации, отсутствии прав доступа или некорректном статусе
        """
        try:
            return await CancelOrderItemCase(db).execute(
                order_item_id=order_item_id,
                user=user,
                cancel_reason=cancel_reason
            )
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc