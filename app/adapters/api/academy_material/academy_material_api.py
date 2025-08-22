from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialWithRelationsRDTO,
    AcademyMaterialCDTO,
    PaginationAcademyMaterialWithRelationsRDTO,
    AcademyMaterialUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.academy_material.academy_material_filter import AcademyMaterialFilter
from app.adapters.filters.academy_material.academy_material_pagination_filter import (
    AcademyMaterialPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy_material.all_academy_materials_case import AllAcademyMaterialsCase
from app.use_case.academy_material.create_academy_material_case import CreateAcademyMaterialCase
from app.use_case.academy_material.delete_academy_material_case import DeleteAcademyMaterialCase
from app.use_case.academy_material.get_academy_material_by_id_case import GetAcademyMaterialByIdCase
from app.use_case.academy_material.paginate_academy_materials_case import PaginateAcademyMaterialsCase
from app.use_case.academy_material.update_academy_material_case import UpdateAcademyMaterialCase


class AcademyMaterialApi:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyMaterialWithRelationsRDTO,
            summary="Список материалов академий с пагинацией",
            description="Получение списка материалов академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyMaterialWithRelationsRDTO],
            summary="Список всех материалов академий",
            description="Получение полного списка материалов академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyMaterialWithRelationsRDTO,
            summary="Создать материал академии",
            description="Создание нового материала академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyMaterialWithRelationsRDTO,
            summary="Обновить материал академии по ID",
            description="Обновление информации о материале академии по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyMaterialWithRelationsRDTO,
            summary="Получить материал академии по ID",
            description="Получение информации о материале академии по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить материал академии по ID",
            description="Удаление материала академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyMaterialPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyMaterialWithRelationsRDTO:
        try:
            return await PaginateAcademyMaterialsCase(db).execute(filter)
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
        filter: AcademyMaterialFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyMaterialWithRelationsRDTO]:
        try:
            return await AllAcademyMaterialsCase(db).execute(filter)
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
        dto: AcademyMaterialCDTO = Depends(FormParserHelper.parse_academy_material_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyMaterialWithRelationsRDTO:
        try:
            return await CreateAcademyMaterialCase(db).execute(dto=dto, file=file)
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
        dto: AcademyMaterialUpdateDTO = Depends(FormParserHelper.parse_academy_material_update_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyMaterialWithRelationsRDTO:
        try:
            return await UpdateAcademyMaterialCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> AcademyMaterialWithRelationsRDTO:
        try:
            return await GetAcademyMaterialByIdCase(db).execute(id=id)
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
            return await DeleteAcademyMaterialCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc