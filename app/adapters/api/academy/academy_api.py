from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyWithRelationsRDTO, AcademyCDTO, GetFullAcademyDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationAcademyWithRelationsRDTO
from app.adapters.filters.academy.academy_filter import AcademyFilter
from app.adapters.filters.academy.academy_pagination_filter import (
    AcademyPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy.all_academies_case import AllAcademiesCase
from app.use_case.academy.create_academy_case import CreateAcademyCase
from app.use_case.academy.delete_academy_case import DeleteAcademyCase
from app.use_case.academy.get_academy_by_id_case import GetAcademyByIdCase
from app.use_case.academy.get_academy_by_value_case import GetAcademyByValueCase
from app.use_case.academy.paginate_academies_case import PaginateAcademiesCase
from app.use_case.academy.update_academy_case import UpdateAcademyCase
from app.use_case.academy.get_full_academy_by_id_case import GetFullAcademyByIdCase
from app.use_case.academy.update_academy_main_photo_case import UpdateAcademyMainPhotoCase


class AcademyApi:
    def __init__(self) -> None:
        """
        Инициализация AcademyApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyWithRelationsRDTO,
            summary="Список академий с пагинацией",
            description="Получение списка академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyWithRelationsRDTO],
            summary="Список всех академий",
            description="Получение полного списка академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyWithRelationsRDTO,
            summary="Создать академию",
            description="Создание новой академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyWithRelationsRDTO,
            summary="Обновить академию по ID",
            description="Обновление информации об академии по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyWithRelationsRDTO,
            summary="Получить академию по ID",
            description="Получение информации об академии по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=AcademyWithRelationsRDTO,
            summary="Получить академию по значению",
            description="Получение информации об академии по уникальному значению (value)",
        )(self.get_by_value)

        self.router.get(
            "/get-full/{id}",
            response_model=GetFullAcademyDTO,
            summary="Получить полную информацию об академии",
            description="Получение полной информации об академии с галереями и группами",
        )(self.get_full_by_id)

        self.router.put(
            "/update-main-photo/{id}",
            response_model=AcademyWithRelationsRDTO,
            summary="Обновить главное изображение академии",
            description="Обновление главного изображения академии по её ID",
        )(self.update_main_photo)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить академию по ID",
            description="Удаление академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyWithRelationsRDTO:
        try:
            return await PaginateAcademiesCase(db).execute(filter)
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
        filter: AcademyFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyWithRelationsRDTO]:
        try:
            return await AllAcademiesCase(db).execute(filter)
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
        dto: AcademyCDTO = Depends(FormParserHelper.parse_academy_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyWithRelationsRDTO:
        try:
            return await CreateAcademyCase(db).execute(dto=dto, file=file)
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
        dto: AcademyCDTO = Depends(FormParserHelper.parse_academy_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyWithRelationsRDTO:
        try:
            return await UpdateAcademyCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> AcademyWithRelationsRDTO:
        try:
            return await GetAcademyByIdCase(db).execute(id=id)
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
    ) -> AcademyWithRelationsRDTO:
        try:
            return await GetAcademyByValueCase(db).execute(value=value)
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
            return await DeleteAcademyCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_full_by_id(
        self,
        id: RoutePathConstants.IDPath,
        force_delete: bool | None = AppQueryConstants.StandardForceDeleteQuery(),
        db: AsyncSession = Depends(get_db),
    ) -> GetFullAcademyDTO:
        try:
            return await GetFullAcademyByIdCase(db).execute(id=id)
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
        file: UploadFile = File(..., description="Файл изображения академии"),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyWithRelationsRDTO:
        try:
            return await UpdateAcademyMainPhotoCase(db).execute(id=id, file=file)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc