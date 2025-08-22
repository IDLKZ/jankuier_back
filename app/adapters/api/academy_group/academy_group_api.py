from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupWithRelationsRDTO, AcademyGroupCDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.academy_group.academy_group_dto import PaginationAcademyGroupWithRelationsRDTO
from app.adapters.filters.academy_group.academy_group_filter import AcademyGroupFilter
from app.adapters.filters.academy_group.academy_group_pagination_filter import (
    AcademyGroupPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy_group.all_academy_groups_case import AllAcademyGroupsCase
from app.use_case.academy_group.create_academy_group_case import CreateAcademyGroupCase
from app.use_case.academy_group.delete_academy_group_case import DeleteAcademyGroupCase
from app.use_case.academy_group.get_academy_group_by_id_case import GetAcademyGroupByIdCase
from app.use_case.academy_group.get_academy_group_by_value_case import GetAcademyGroupByValueCase
from app.use_case.academy_group.paginate_academy_groups_case import PaginateAcademyGroupsCase
from app.use_case.academy_group.update_academy_group_case import UpdateAcademyGroupCase


class AcademyGroupApi:
    def __init__(self) -> None:
        """
        Инициализация AcademyGroupApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API групп академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyGroupWithRelationsRDTO,
            summary="Список групп академий с пагинацией",
            description="Получение списка групп академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyGroupWithRelationsRDTO],
            summary="Список всех групп академий",
            description="Получение полного списка групп академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyGroupWithRelationsRDTO,
            summary="Создать группу академии",
            description="Создание новой группы академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyGroupWithRelationsRDTO,
            summary="Обновить группу академии по ID",
            description="Обновление информации о группе академии по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyGroupWithRelationsRDTO,
            summary="Получить группу академии по ID",
            description="Получение информации о группе академии по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=AcademyGroupWithRelationsRDTO,
            summary="Получить группу академии по значению",
            description="Получение информации о группе академии по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить группу академии по ID",
            description="Удаление группы академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyGroupPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyGroupWithRelationsRDTO:
        try:
            return await PaginateAcademyGroupsCase(db).execute(filter)
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
        filter: AcademyGroupFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyGroupWithRelationsRDTO]:
        try:
            return await AllAcademyGroupsCase(db).execute(filter)
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
        dto: AcademyGroupCDTO = Depends(FormParserHelper.parse_academy_group_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupWithRelationsRDTO:
        try:
            return await CreateAcademyGroupCase(db).execute(dto=dto, file=file)
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
        dto: AcademyGroupCDTO = Depends(FormParserHelper.parse_academy_group_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupWithRelationsRDTO:
        try:
            return await UpdateAcademyGroupCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> AcademyGroupWithRelationsRDTO:
        try:
            return await GetAcademyGroupByIdCase(db).execute(id=id)
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
    ) -> AcademyGroupWithRelationsRDTO:
        try:
            return await GetAcademyGroupByValueCase(db).execute(value=value)
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
            return await DeleteAcademyGroupCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc