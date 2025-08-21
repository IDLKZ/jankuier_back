from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from packaging.utils import _
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.permission.permission_dto import PermissionRDTO, PermissionCDTO
from app.adapters.dto.pagination_dto import PaginationPermissionRDTO
from app.adapters.filters.permission.permission_filter import PermissionFilter
from app.adapters.filters.permission.permission_pagination_filter import (
    PermissionPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.permission.all_permission_case import AllPermissionCase
from app.use_case.permission.create_permission_case import CreatePermissionCase
from app.use_case.permission.delete_permission_case import DeletePermissionByIdCase
from app.use_case.permission.get_permission_by_id_case import GetPermissionByIdCase
from app.use_case.permission.get_permission_by_value_case import (
    GetPermissionByValueCase,
)
from app.use_case.permission.paginate_permission_case import PaginatePermissionCase
from app.use_case.permission.update_permission_case import UpdatePermissionCase


class PermissionApi:
    def __init__(self) -> None:
        """
        Инициализация PermissionApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API permission.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationPermissionRDTO,
            summary="Список разрешений с пагинацией",
            description="Получение списка разрешений с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[PermissionRDTO],
            summary="Список всех разрешений",
            description="Получение полного списка разрешений",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=PermissionRDTO,
            summary="Создать разрешение",
            description="Создание нового разрешения",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=PermissionRDTO,
            summary="Обновить разрешение по ID",
            description="Обновление информации о разрешении по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=PermissionRDTO,
            summary="Получить разрешение по ID",
            description="Получение информации о разрешении по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=PermissionRDTO,
            summary="Получить разрешение по значению",
            description="Получение информации о разрешении по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить разрешение по ID",
            description="Удаление разрешения по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: PermissionPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationPermissionRDTO:
        try:
            return await PaginatePermissionCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: PermissionFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[PermissionRDTO]:
        try:
            return await AllPermissionCase(db).execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: PermissionCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> PermissionRDTO:
        try:
            return await CreatePermissionCase(db).execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: PermissionCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> PermissionRDTO:
        try:
            return await UpdatePermissionCase(db).execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_id(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> PermissionRDTO:
        try:
            return await GetPermissionByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_value(
        self,
        value: RoutePathConstants.ValuePath,
        db: AsyncSession = Depends(get_db),
    ) -> PermissionRDTO:
        try:
            return await GetPermissionByValueCase(db).execute(value=value)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
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
            return await DeletePermissionByIdCase(db).execute(
                id=id, force_delete=force_delete
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
