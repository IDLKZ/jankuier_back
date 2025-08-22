from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_gallery.academy_gallery_dto import (
    AcademyGalleryWithRelationsRDTO,
    AcademyGalleryCDTO,
    PaginationAcademyGalleryWithRelationsRDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.academy_gallery.academy_gallery_filter import AcademyGalleryFilter
from app.adapters.filters.academy_gallery.academy_gallery_pagination_filter import (
    AcademyGalleryPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy_gallery.all_academy_galleries_case import AllAcademyGalleriesCase
from app.use_case.academy_gallery.create_academy_gallery_case import CreateAcademyGalleryCase
from app.use_case.academy_gallery.delete_academy_gallery_case import DeleteAcademyGalleryCase
from app.use_case.academy_gallery.get_academy_gallery_by_id_case import GetAcademyGalleryByIdCase
from app.use_case.academy_gallery.paginate_academy_galleries_case import PaginateAcademyGalleriesCase
from app.use_case.academy_gallery.update_academy_gallery_case import UpdateAcademyGalleryCase


class AcademyGalleryApi:
    def __init__(self) -> None:
        """
        Инициализация AcademyGalleryApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API галереи академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyGalleryWithRelationsRDTO,
            summary="Список изображений галереи академий с пагинацией",
            description="Получение списка изображений галереи академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyGalleryWithRelationsRDTO],
            summary="Список всех изображений галереи академий",
            description="Получение полного списка изображений галереи академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyGalleryWithRelationsRDTO,
            summary="Создать изображение галереи академии",
            description="Создание нового изображения в галерее академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyGalleryWithRelationsRDTO,
            summary="Обновить изображение галереи академии по ID",
            description="Обновление информации об изображении галереи академии по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyGalleryWithRelationsRDTO,
            summary="Получить изображение галереи академии по ID",
            description="Получение информации об изображении галереи академии по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить изображение галереи академии по ID",
            description="Удаление изображения галереи академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyGalleryPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyGalleryWithRelationsRDTO:
        try:
            return await PaginateAcademyGalleriesCase(db).execute(filter)
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
        filter: AcademyGalleryFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyGalleryWithRelationsRDTO]:
        try:
            return await AllAcademyGalleriesCase(db).execute(filter)
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
        dto: AcademyGalleryCDTO = Depends(FormParserHelper.parse_academy_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGalleryWithRelationsRDTO:
        try:
            return await CreateAcademyGalleryCase(db).execute(dto=dto, file=file)
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
        dto: AcademyGalleryCDTO = Depends(FormParserHelper.parse_academy_gallery_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGalleryWithRelationsRDTO:
        try:
            return await UpdateAcademyGalleryCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> AcademyGalleryWithRelationsRDTO:
        try:
            return await GetAcademyGalleryByIdCase(db).execute(id=id)
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
            return await DeleteAcademyGalleryCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc