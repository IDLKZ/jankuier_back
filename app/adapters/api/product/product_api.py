from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO, ProductCDTO
from app.adapters.dto.product.full_product_dto import FullProductRDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationProductWithRelationsRDTO
from app.adapters.filters.product.product_filter import ProductFilter
from app.adapters.filters.product.product_pagination_filter import (
    ProductPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product.all_product_case import AllProductCase
from app.use_case.product.create_product_case import CreateProductCase
from app.use_case.product.delete_product_case import DeleteProductCase
from app.use_case.product.get_product_by_id_case import GetProductByIdCase
from app.use_case.product.get_product_by_value_case import GetProductByValueCase
from app.use_case.product.paginate_product_case import PaginateProductCase
from app.use_case.product.update_product_case import UpdateProductCase
from app.use_case.product.get_full_product_by_id_case import GetFullProductByIdCase
from app.use_case.product.update_product_main_photo_case import UpdateProductMainPhotoCase


class ProductApi:
    def __init__(self) -> None:
        """
        Инициализация ProductApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API товаров.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductWithRelationsRDTO,
            summary="Список товаров с пагинацией",
            description="Получение списка товаров с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ProductWithRelationsRDTO],
            summary="Список всех товаров",
            description="Получение полного списка товаров",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ProductWithRelationsRDTO,
            summary="Создать товар",
            description="Создание нового товара",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductWithRelationsRDTO,
            summary="Обновить товар по ID",
            description="Обновление информации о товаре по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductWithRelationsRDTO,
            summary="Получить товар по ID",
            description="Получение информации о товаре по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=ProductWithRelationsRDTO,
            summary="Получить товар по значению",
            description="Получение информации о товаре по уникальному значению (value)",
        )(self.get_by_value)

        self.router.get(
            RoutePathConstants.GetFullProductByIdPathName,
            response_model=FullProductRDTO,
            summary="Получить полную информацию о товаре по ID",
            description="Получение полной информации о товаре включая галерею, варианты и модификации",
        )(self.get_full_product_by_id)

        self.router.put(
            "/update-main-photo/{id}",
            response_model=ProductWithRelationsRDTO,
            summary="Обновить главное изображение товара",
            description="Обновление главного изображения товара по его ID",
        )(self.update_main_photo)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить товар по ID",
            description="Удаление товара по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ProductPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductWithRelationsRDTO:
        try:
            return await PaginateProductCase(db).execute(filter)
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
        filter: ProductFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductWithRelationsRDTO]:
        try:
            return await AllProductCase(db).execute(filter)
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
        dto: ProductCDTO = Depends(FormParserHelper.parse_product_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductWithRelationsRDTO:
        try:
            return await CreateProductCase(db).execute(dto=dto, file=file)
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
        dto: ProductCDTO = Depends(FormParserHelper.parse_product_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductWithRelationsRDTO:
        try:
            return await UpdateProductCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> ProductWithRelationsRDTO:
        try:
            return await GetProductByIdCase(db).execute(id=id)
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
    ) -> ProductWithRelationsRDTO:
        try:
            return await GetProductByValueCase(db).execute(value=value)
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
            return await DeleteProductCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_full_product_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> FullProductRDTO:
        try:
            return await GetFullProductByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update_main_photo(
        self,
        id: RoutePathConstants.IDPath,
        file: UploadFile = File(..., description="Файл изображения товара"),
        db: AsyncSession = Depends(get_db),
    ) -> ProductWithRelationsRDTO:
        try:
            return await UpdateProductMainPhotoCase(db).execute(id=id, file=file)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
