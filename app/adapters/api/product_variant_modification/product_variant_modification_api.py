from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant_modification.product_variant_modification_dto import (
    ProductVariantModificationWithRelationsRDTO,
    ProductVariantModificationCDTO,
)
from app.adapters.dto.pagination_dto import (
    PaginationProductVariantModificationWithRelationsRDTO,
)
from app.adapters.filters.product_variant_modification.product_variant_modification_filter import (
    ProductVariantModificationFilter,
)
from app.adapters.filters.product_variant_modification.product_variant_modification_pagination_filter import (
    ProductVariantModificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_variant_modification.all_product_variant_modification_case import (
    AllProductVariantModificationCase,
)
from app.use_case.product_variant_modification.create_product_variant_modification_case import (
    CreateProductVariantModificationCase,
)
from app.use_case.product_variant_modification.delete_product_variant_modification_case import (
    DeleteProductVariantModificationCase,
)
from app.use_case.product_variant_modification.get_product_variant_modification_by_id_case import (
    GetProductVariantModificationByIdCase,
)
from app.use_case.product_variant_modification.paginate_product_variant_modification_case import (
    PaginateProductVariantModificationCase,
)
from app.use_case.product_variant_modification.update_product_variant_modification_case import (
    UpdateProductVariantModificationCase,
)


class ProductVariantModificationApi:
    def __init__(self) -> None:
        """
        Инициализация ProductVariantModificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API модификаций вариантов товаров.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductVariantModificationWithRelationsRDTO,
            summary="Список модификаций вариантов товаров с пагинацией",
            description="Получение списка модификаций вариантов товаров с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ProductVariantModificationWithRelationsRDTO],
            summary="Список всех модификаций вариантов товаров",
            description="Получение полного списка модификаций вариантов товаров",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ProductVariantModificationWithRelationsRDTO,
            summary="Создать модификацию варианта товара",
            description="Создание новой модификации варианта товара",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductVariantModificationWithRelationsRDTO,
            summary="Обновить модификацию варианта товара по ID",
            description="Обновление информации о модификации варианта товара по её ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductVariantModificationWithRelationsRDTO,
            summary="Получить модификацию варианта товара по ID",
            description="Получение информации о модификации варианта товара по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить модификацию варианта товара по ID",
            description="Удаление модификации варианта товара по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ProductVariantModificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductVariantModificationWithRelationsRDTO:
        try:
            return await PaginateProductVariantModificationCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: ProductVariantModificationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductVariantModificationWithRelationsRDTO]:
        try:
            return await AllProductVariantModificationCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: ProductVariantModificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantModificationWithRelationsRDTO:
        try:
            return await CreateProductVariantModificationCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: ProductVariantModificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantModificationWithRelationsRDTO:
        try:
            return await UpdateProductVariantModificationCase(db).execute(
                id=id, dto=dto
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantModificationWithRelationsRDTO:
        try:
            return await GetProductVariantModificationByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        try:
            return await DeleteProductVariantModificationCase(db).execute(
                id=id, force_delete=force_delete
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
