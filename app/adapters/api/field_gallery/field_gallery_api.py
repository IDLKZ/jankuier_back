from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_gallery.field_gallery_dto import FieldGalleryWithRelationsRDTO, FieldGalleryCDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationFieldGalleryWithRelationsRDTO
from app.adapters.filters.field_gallery.field_gallery_filter import FieldGalleryFilter
from app.adapters.filters.field_gallery.field_gallery_pagination_filter import (
    FieldGalleryPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.field_gallery.all_field_galleries_case import AllFieldGalleriesCase
from app.use_case.field_gallery.create_field_gallery_case import CreateFieldGalleryCase
from app.use_case.field_gallery.delete_field_gallery_case import DeleteFieldGalleryCase
from app.use_case.field_gallery.get_field_gallery_by_id_case import GetFieldGalleryByIdCase
from app.use_case.field_gallery.paginate_field_galleries_case import PaginateFieldGalleriesCase
from app.use_case.field_gallery.update_field_gallery_case import UpdateFieldGalleryCase


class FieldGalleryApi:
    def __init__(self) -> None:
        """
        Инициализация FieldGalleryApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API галереи полей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFieldGalleryWithRelationsRDTO,
            summary="Список изображений галереи полей с пагинацией",
            description="Получение списка изображений галереи полей с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[FieldGalleryWithRelationsRDTO],
            summary="Список всех изображений галереи полей",
            description="Получение полного списка изображений галереи полей",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FieldGalleryWithRelationsRDTO,
            summary="Создать изображение галереи поля",
            description="Создание нового изображения в галерее поля",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FieldGalleryWithRelationsRDTO,
            summary="Обновить изображение галереи поля по ID",
            description="Обновление информации об изображении галереи поля по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FieldGalleryWithRelationsRDTO,
            summary="Получить изображение галереи поля по ID",
            description="Получение информации об изображении галереи поля по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить изображение галереи поля по ID",
            description="Удаление изображения галереи поля по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: FieldGalleryPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFieldGalleryWithRelationsRDTO:
        try:
            return await PaginateFieldGalleriesCase(db).execute(filter)
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
        filter: FieldGalleryFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[FieldGalleryWithRelationsRDTO]:
        try:
            return await AllFieldGalleriesCase(db).execute(filter)
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
        dto: FieldGalleryCDTO = Depends(FormParserHelper.parse_field_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldGalleryWithRelationsRDTO:
        try:
            return await CreateFieldGalleryCase(db).execute(dto=dto, file=file)
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
        dto: FieldGalleryCDTO = Depends(FormParserHelper.parse_field_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldGalleryWithRelationsRDTO:
        try:
            return await UpdateFieldGalleryCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> FieldGalleryWithRelationsRDTO:
        try:
            return await GetFieldGalleryByIdCase(db).execute(id=id)
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
            return await DeleteFieldGalleryCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc