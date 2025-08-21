from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_variant.product_variant_dto import (
    ProductVariantWithRelationsRDTO,
    ProductVariantCDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationProductVariantWithRelationsRDTO
from app.adapters.filters.product_variant.product_variant_filter import (
    ProductVariantFilter,
)
from app.adapters.filters.product_variant.product_variant_pagination_filter import (
    ProductVariantPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_variant.all_product_variant_case import AllProductVariantCase
from app.use_case.product_variant.create_product_variant_case import (
    CreateProductVariantCase,
)
from app.use_case.product_variant.delete_product_variant_case import (
    DeleteProductVariantCase,
)
from app.use_case.product_variant.get_product_variant_by_id_case import (
    GetProductVariantByIdCase,
)
from app.use_case.product_variant.get_product_variant_by_value_case import (
    GetProductVariantByValueCase,
)
from app.use_case.product_variant.paginate_product_variant_case import (
    PaginateProductVariantCase,
)
from app.use_case.product_variant.update_product_variant_case import (
    UpdateProductVariantCase,
)


class ProductVariantApi:
    def __init__(self) -> None:
        """
        Инициализация ProductVariantApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API вариантов товаров.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductVariantWithRelationsRDTO,
            summary="Список вариантов товаров с пагинацией",
            description="Получение списка вариантов товаров с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ProductVariantWithRelationsRDTO],
            summary="Список всех вариантов товаров",
            description="Получение полного списка вариантов товаров",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ProductVariantWithRelationsRDTO,
            summary="Создать вариант товара",
            description="Создание нового варианта товара",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductVariantWithRelationsRDTO,
            summary="Обновить вариант товара по ID",
            description="Обновление информации о варианте товара по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductVariantWithRelationsRDTO,
            summary="Получить вариант товара по ID",
            description="Получение информации о варианте товара по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=ProductVariantWithRelationsRDTO,
            summary="Получить вариант товара по значению",
            description="Получение информации о варианте товара по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить вариант товара по ID",
            description="Удаление варианта товара по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ProductVariantPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductVariantWithRelationsRDTO:
        try:
            return await PaginateProductVariantCase(db).execute(filter)
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
        filter: ProductVariantFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductVariantWithRelationsRDTO]:
        try:
            return await AllProductVariantCase(db).execute(filter)
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
        dto: ProductVariantCDTO = Depends(FormParserHelper.parse_product_variant_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantWithRelationsRDTO:
        try:
            return await CreateProductVariantCase(db).execute(dto=dto, file=file)
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
        dto: ProductVariantCDTO = Depends(FormParserHelper.parse_product_variant_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantWithRelationsRDTO:
        try:
            return await UpdateProductVariantCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> ProductVariantWithRelationsRDTO:
        try:
            return await GetProductVariantByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_value(
        self,
        value: RoutePathConstants.ValuePath,
        db: AsyncSession = Depends(get_db),
    ) -> ProductVariantWithRelationsRDTO:
        try:
            return await GetProductVariantByValueCase(db).execute(value=value)
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
            return await DeleteProductVariantCase(db).execute(
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
