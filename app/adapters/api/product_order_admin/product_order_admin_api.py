import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderWithRelationsRDTO
from app.adapters.dto.product_order.product_order_dto import ProductOrderCDTO, ProductOrderWithRelationsRDTO
from app.adapters.filters.product_order.product_order_pagination_filter import ProductOrderPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order.admin.delete_product_order_case import DeleteProductOrderCase
from app.use_case.product_order.admin.get_product_order_by_id_case import GetProductOrderByIdCase
from app.use_case.product_order.admin.paginate_product_order_case import PaginateProductOrderCase
from app.use_case.product_order.admin.update_product_order_case import UpdateProductOrderCase


class ProductOrderAdminApi:
    """
    API контроллер для управления заказами (админ).

    Предоставляет CRUD операции для заказов:
    - Получение списка заказов с пагинацией
    - Получение заказа по ID
    - Обновление заказа
    - Удаление заказа

    Доступ только для администраторов.
    """

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """Регистрация маршрутов API"""

        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductOrderWithRelationsRDTO,
            summary="Список заказов (админ)",
            description="Получение пагинированного списка всех заказов системы с возможностью фильтрации",
        )(self.paginate_orders)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductOrderWithRelationsRDTO,
            summary="Получить заказ по ID (админ)",
            description="Получение заказа по его идентификатору с полной информацией и связями",
        )(self.get_order_by_id)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductOrderWithRelationsRDTO,
            summary="Обновить заказ (админ)",
            description="Обновление информации о заказе",
        )(self.update_order)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить заказ (админ)",
            description="Удаление заказа из системы (мягкое или жесткое удаление)",
        )(self.delete_order)

    async def paginate_orders(
        self,
        filter_obj: ProductOrderPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductOrderWithRelationsRDTO:
        """
        Получение пагинированного списка заказов.

        Args:
            filter_obj: Объект фильтрации и пагинации заказов
            db: Сессия базы данных

        Returns:
            PaginationProductOrderWithRelationsRDTO: Пагинированный список заказов

        Raises:
            HTTPException: При ошибках валидации или внутренних ошибках
        """
        try:
            return await PaginateProductOrderCase(db).execute(filter_obj=filter_obj)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_order_by_id(
        self,
        id: RoutePathConstants.IDPath,
        include_deleted: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderWithRelationsRDTO:
        """
        Получение заказа по ID.

        Args:
            id: ID заказа для получения
            include_deleted: Включать удаленные записи
            db: Сессия базы данных

        Returns:
            ProductOrderWithRelationsRDTO: Заказ с полными relationships

        Raises:
            HTTPException: При ошибках валидации, отсутствии заказа
        """
        try:
            return await GetProductOrderByIdCase(db).execute(
                order_id=id, include_deleted=include_deleted or False
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

    async def update_order(
        self,
        id: RoutePathConstants.IDPath,
        dto: ProductOrderCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderWithRelationsRDTO:
        """
        Обновление заказа.

        Args:
            id: ID заказа для обновления
            dto: DTO с данными для обновления
            db: Сессия базы данных

        Returns:
            ProductOrderWithRelationsRDTO: Обновленный заказ с relationships

        Raises:
            HTTPException: При ошибках валидации, отсутствии заказа
        """
        try:
            return await UpdateProductOrderCase(db).execute(order_id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete_order(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Удаление заказа.

        Args:
            id: ID заказа для удаления
            force_delete: Флаг для полного удаления
            db: Сессия базы данных

        Returns:
            bool: True при успешном удалении

        Raises:
            HTTPException: При ошибках валидации, отсутствии заказа
        """
        try:
            return await DeleteProductOrderCase(db).execute(
                order_id=id, force_delete=force_delete or False
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