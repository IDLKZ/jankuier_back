from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.product_order_item_status.product_order_item_status_dto import ProductOrderItemStatusWithRelationsRDTO, ProductOrderItemStatusCDTO
from app.adapters.filters.product_order_item_status.product_order_item_status_filter import ProductOrderItemStatusFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import _
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order_item_status.all_product_order_item_status_case import AllProductOrderItemStatusCase
from app.use_case.product_order_item_status.create_product_order_item_status_case import CreateProductOrderItemStatusCase
from app.use_case.product_order_item_status.delete_product_order_item_status_case import DeleteProductOrderItemStatusCase
from app.use_case.product_order_item_status.get_product_order_item_status_by_id_case import GetProductOrderItemStatusByIdCase
from app.use_case.product_order_item_status.update_product_order_item_status_case import UpdateProductOrderItemStatusCase


class ProductOrderItemStatusApi:

    def __init__(self) -> None:
        """
        Инициализация ProductOrderItemStatusApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API статусов элементов заказов.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=list[ProductOrderItemStatusWithRelationsRDTO],
            summary="Список статусов элементов заказов",
            description="Получение списка статусов элементов заказов",
        )(self.get_all)
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=ProductOrderItemStatusWithRelationsRDTO,
            summary="Создать статус элемента заказа",
            description="Создание статуса элемента заказа",
        )(self.create)
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=ProductOrderItemStatusWithRelationsRDTO,
            summary="Обновить статус элемента заказа по ID",
            description="Обновление статуса элемента заказа по ID",
        )(self.update)
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=ProductOrderItemStatusWithRelationsRDTO,
            summary="Получить статус элемента заказа по ID",
            description="Получение статуса элемента заказа по ID",
        )(self.get)
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить статус элемента заказа по ID",
            description="Удаление статуса элемента заказа по ID",
        )(self.delete)

    async def get_all(
        self,
        filter: ProductOrderItemStatusFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductOrderItemStatusWithRelationsRDTO]:
        use_case = AllProductOrderItemStatusCase(db)
        try:
            return await use_case.execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: ProductOrderItemStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemStatusWithRelationsRDTO:
        use_case = CreateProductOrderItemStatusCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: ProductOrderItemStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemStatusWithRelationsRDTO:
        use_case = UpdateProductOrderItemStatusCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderItemStatusWithRelationsRDTO:
        use_case = GetProductOrderItemStatusByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        use_case = DeleteProductOrderItemStatusCase(db)
        try:
            return await use_case.execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc