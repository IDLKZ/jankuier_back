from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.product_order_status.product_order_status_dto import ProductOrderStatusWithRelationsRDTO, ProductOrderStatusCDTO
from app.adapters.filters.product_order_status.product_order_status_filter import ProductOrderStatusFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import _
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order_status.all_product_order_status_case import AllProductOrderStatusCase
from app.use_case.product_order_status.create_product_order_status_case import CreateProductOrderStatusCase
from app.use_case.product_order_status.delete_product_order_status_case import DeleteProductOrderStatusCase
from app.use_case.product_order_status.get_product_order_status_by_id_case import GetProductOrderStatusByIdCase
from app.use_case.product_order_status.update_product_order_status_case import UpdateProductOrderStatusCase


class ProductOrderStatusApi:

    def __init__(self) -> None:
        """
        Инициализация ProductOrderStatusApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API статусов заказов.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=list[ProductOrderStatusWithRelationsRDTO],
            summary="Список статусов заказов",
            description="Получение списка статусов заказов",
        )(self.get_all)
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=ProductOrderStatusWithRelationsRDTO,
            summary="Создать статус заказа",
            description="Создание статуса заказа",
        )(self.create)
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=ProductOrderStatusWithRelationsRDTO,
            summary="Обновить статус заказа по ID",
            description="Обновление статуса заказа по ID",
        )(self.update)
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=ProductOrderStatusWithRelationsRDTO,
            summary="Получить статус заказа по ID",
            description="Получение статуса заказа по ID",
        )(self.get)
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалить статус заказа по ID",
            description="Удаление статуса заказа по ID",
        )(self.delete)

    async def get_all(
        self,
        filter: ProductOrderStatusFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductOrderStatusWithRelationsRDTO]:
        use_case = AllProductOrderStatusCase(db)
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
        dto: ProductOrderStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderStatusWithRelationsRDTO:
        use_case = CreateProductOrderStatusCase(db)
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
        dto: ProductOrderStatusCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderStatusWithRelationsRDTO:
        use_case = UpdateProductOrderStatusCase(db)
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
    ) -> ProductOrderStatusWithRelationsRDTO:
        use_case = GetProductOrderStatusByIdCase(db)
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
        use_case = DeleteProductOrderStatusCase(db)
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