from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryWithRelationsRDTO, ProductGalleryCDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationProductGalleryWithRelationsRDTO
from app.adapters.filters.product_gallery.product_gallery_filter import ProductGalleryFilter
from app.adapters.filters.product_gallery.product_gallery_pagination_filter import (
    ProductGalleryPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_gallery.all_product_gallery_case import AllProductGalleryCase
from app.use_case.product_gallery.create_product_gallery_case import CreateProductGalleryCase
from app.use_case.product_gallery.delete_product_gallery_case import DeleteProductGalleryCase
from app.use_case.product_gallery.get_product_gallery_by_id_case import GetProductGalleryByIdCase
from app.use_case.product_gallery.paginate_product_gallery_case import PaginateProductGalleryCase
from app.use_case.product_gallery.update_product_gallery_case import UpdateProductGalleryCase


class ProductGalleryApi:
    def __init__(self) -> None:
        """
        Инициализация ProductGalleryApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API галереи товаров.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationProductGalleryWithRelationsRDTO,
            summary="Список изображений галереи с пагинацией",
            description="Получение списка изображений галереи товаров с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ProductGalleryWithRelationsRDTO],
            summary="Список всех изображений галереи",
            description="Получение полного списка изображений галереи товаров",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ProductGalleryWithRelationsRDTO,
            summary="Создать изображение галереи",
            description="Создание нового изображения в галерее товара",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ProductGalleryWithRelationsRDTO,
            summary="Обновить изображение галереи по ID",
            description="Обновление информации об изображении галереи по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ProductGalleryWithRelationsRDTO,
            summary="Получить изображение галереи по ID",
            description="Получение информации об изображении галереи по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить изображение галереи по ID",
            description="Удаление изображения галереи по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ProductGalleryPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationProductGalleryWithRelationsRDTO:
        try:
            return await PaginateProductGalleryCase(db).execute(filter)
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
        filter: ProductGalleryFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ProductGalleryWithRelationsRDTO]:
        try:
            return await AllProductGalleryCase(db).execute(filter)
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
        dto: ProductGalleryCDTO = Depends(FormParserHelper.parse_product_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductGalleryWithRelationsRDTO:
        try:
            return await CreateProductGalleryCase(db).execute(dto=dto, file=file)
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
        dto: ProductGalleryCDTO = Depends(FormParserHelper.parse_product_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> ProductGalleryWithRelationsRDTO:
        try:
            return await UpdateProductGalleryCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> ProductGalleryWithRelationsRDTO:
        try:
            return await GetProductGalleryByIdCase(db).execute(id=id)
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
            return await DeleteProductGalleryCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc