import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.pagination_dto import PaginationProductOrderItemWithRelationsRDTO
from app.adapters.dto.product_order_item.product_order_item_dto import ProductOrderItemCDTO, ProductOrderItemWithRelationsRDTO
from app.adapters.filters.product_order_item.product_order_item_pagination_filter import ProductOrderItemPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order_item.admin.delete_product_order_item_case import DeleteProductOrderItemCase
from app.use_case.product_order_item.admin.get_product_order_item_by_id_case import GetProductOrderItemByIdCase
from app.use_case.product_order_item.admin.paginate_product_order_item_case import PaginateProductOrderItemCase
from app.use_case.product_order_item.admin.update_product_order_item_case import UpdateProductOrderItemCase


class ProductOrderItemAdminApi:
    """
    API контроллер для управления элементами заказов (админ).

    Предоставляет CRUD операции для элементов заказов:
    - Получение списка элементов заказов с пагинацией
    - Получение элемента заказа по ID
    - Обновление элемента заказа
    - Удаление элемента заказа

    Доступ только для администраторов.
    """

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """Регистрация маршрутов API"""

        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductOrderItemWithRelationsRDTO,
            summary="Список элементов заказов (админ)",
            description="Получение пагинированного списка всех элементов заказов системы с возможностью фильтрации",
        )(self.paginate_order_items)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductOrderItemWithRelationsRDTO,
            summary="Получить элемент заказа по ID (админ)",
            description="Получение элемента заказа по его идентификатору с полной информацией и связями",
        )(self.get_order_item_by_id)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductOrderItemWithRelationsRDTO,
            summary="Обновить элемент заказа (админ)",
            description="Обновление информации об элементе заказа",
        )(self.update_order_item)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить элемент заказа (админ)",
            description="Удаление элемента заказа из системы (мягкое или жесткое удаление)",
        )(self.delete_order_item)

    async def paginate_order_items(
        self,
        filter_obj: ProductOrderItemPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductOrderItemWithRelationsRDTO:
        """
        Получение пагинированного списка элементов заказов.

        Args:
            filter_obj: Объект фильтрации и пагинации элементов заказов
            db: Сессия базы данных

        Returns:
            PaginationProductOrderItemWithRelationsRDTO: Пагинированный список элементов заказов

        Raises:
            HTTPException: При ошибках валидации или внутренних ошибках
        """
        try:
            return await PaginateProductOrderItemCase(db).execute(filter_obj=filter_obj)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_order_item_by_id(
        self,
        id: RoutePathConstants.IDPath,
        include_deleted: bool | None = AppQueryConstants.StandardOptionalBooleanQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemWithRelationsRDTO:
        """
        Получение элемента заказа по ID.

        Args:
            id: ID элемента заказа для получения
            include_deleted: Включать удаленные записи
            db: Сессия базы данных

        Returns:
            ProductOrderItemWithRelationsRDTO: Элемент заказа с полными relationships

        Raises:
            HTTPException: При ошибках валидации, отсутствии элемента заказа
        """
        try:
            return await GetProductOrderItemByIdCase(db).execute(
                item_id=id, include_deleted=include_deleted or False
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

    async def update_order_item(
        self,
        id: RoutePathConstants.IDPath,
        dto: ProductOrderItemCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemWithRelationsRDTO:
        """
        Обновление элемента заказа.

        Args:
            id: ID элемента заказа для обновления
            dto: DTO с данными для обновления
            db: Сессия базы данных

        Returns:
            ProductOrderItemWithRelationsRDTO: Обновленный элемент заказа с relationships

        Raises:
            HTTPException: При ошибках валидации, отсутствии элемента заказа
        """
        try:
            return await UpdateProductOrderItemCase(db).execute(item_id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete_order_item(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        """
        Удаление элемента заказа.

        Args:
            id: ID элемента заказа для удаления
            force_delete: Флаг для полного удаления
            db: Сессия базы данных

        Returns:
            bool: True при успешном удалении

        Raises:
            HTTPException: При ошибках валидации, отсутствии элемента заказа
        """
        try:
            return await DeleteProductOrderItemCase(db).execute(
                item_id=id, force_delete=force_delete or False
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