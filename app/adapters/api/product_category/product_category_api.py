from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_category.product_category_dto import (
    ProductCategoryWithRelationsRDTO,
    ProductCategoryCDTO,
)
from app.adapters.dto.pagination_dto import PaginationProductCategoryWithRelationsRDTO
from app.adapters.filters.product_category.product_category_filter import (
    ProductCategoryFilter,
)
from app.adapters.filters.product_category.product_category_pagination_filter import (
    ProductCategoryPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.helpers.form_helper import FormParserHelper
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_category.all_product_category_case import (
    AllProductCategoryCase,
)
from app.use_case.product_category.create_product_category_case import (
    CreateProductCategoryCase,
)
from app.use_case.product_category.delete_product_category_case import (
    DeleteProductCategoryCase,
)
from app.use_case.product_category.get_product_category_by_id_case import (
    GetProductCategoryByIdCase,
)
from app.use_case.product_category.get_product_category_by_value_case import (
    GetProductCategoryByValueCase,
)
from app.use_case.product_category.paginate_product_category_case import (
    PaginateProductCategoryCase,
)
from app.use_case.product_category.update_product_category_case import (
    UpdateProductCategoryCase,
)


class ProductCategoryApi:
    def __init__(self) -> None:
        """
        Инициализация ProductCategoryApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API категорий товаров.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductCategoryWithRelationsRDTO,
            summary="Список категорий товаров с пагинацией",
            description="Получение списка категорий товаров с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ProductCategoryWithRelationsRDTO],
            summary="Список всех категорий товаров",
            description="Получение полного списка категорий товаров",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ProductCategoryWithRelationsRDTO,
            summary="Создать категорию товара",
            description="Создание новой категории товара",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductCategoryWithRelationsRDTO,
            summary="Обновить категорию товара по ID",
            description="Обновление информации о категории товара по её ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductCategoryWithRelationsRDTO,
            summary="Получить категорию товара по ID",
            description="Получение информации о категории товара по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=ProductCategoryWithRelationsRDTO,
            summary="Получить категорию товара по значению",
            description="Получение информации о категории товара по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить категорию товара по ID",
            description="Удаление категории товара по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ProductCategoryPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductCategoryWithRelationsRDTO:
        try:
            return await PaginateProductCategoryCase(db).execute(filter)
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
        filter: ProductCategoryFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductCategoryWithRelationsRDTO]:
        try:
            return await AllProductCategoryCase(db).execute(filter)
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
        dto: ProductCategoryCDTO = Depends(FormParserHelper.parse_product_category_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductCategoryWithRelationsRDTO:
        try:
            return await CreateProductCategoryCase(db).execute(dto=dto, file=file)
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
        dto: ProductCategoryCDTO = Depends(FormParserHelper.parse_product_category_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductCategoryWithRelationsRDTO:
        try:
            return await UpdateProductCategoryCase(db).execute(
                id=id, dto=dto, file=file
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
    ) -> ProductCategoryWithRelationsRDTO:
        try:
            return await GetProductCategoryByIdCase(db).execute(id=id)
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
    ) -> ProductCategoryWithRelationsRDTO:
        try:
            return await GetProductCategoryByValueCase(db).execute(value=value)
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
            return await DeleteProductCategoryCase(db).execute(
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
