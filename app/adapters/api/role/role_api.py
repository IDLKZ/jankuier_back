from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.adapters.dto.role.role_dto import RoleRDTO, RoleCDTO
from app.adapters.filters.role.role_filter import RoleFilter
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import AppTranslationsWrapper, _
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.role.all_role_case import AllRoleCase
from app.use_case.role.create_role_case import CreateRoleCase
from app.use_case.role.delete_role_case import DeleteRoleByIdCase
from app.use_case.role.get_by_id_case import GetRoleByIdCase
from app.use_case.role.get_role_by_value_case import GetRoleByValueCase
from app.use_case.role.update_role_case import UpdateRoleCase


class RoleApi:

    def __init__(self) -> None:
        """
        Инициализация RoleApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API ролей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=list[RoleRDTO],
            summary="Список ролей",
            description="Получение списка ролей",
        )(self.get_all)
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=RoleRDTO,
            summary="Создать роль",
            description="Создание роли",
        )(self.create)
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=RoleRDTO,
            summary="Обновить роль по ID",
            description="Обновление роли по ID",
        )(self.update)
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=RoleRDTO,
            summary="Получить роль по ID",
            description="Получение роли по ID",
        )(self.get)
        self.router.get(
            f"{RoutePathConstants.GetByValuePathName}",
            response_model=RoleRDTO,
            summary="Получить роль по уникальному значению",
            description="Получение роль по уникальному значению",
        )(self.get_by_value)
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите роль по ID",
            description="Удаление роли по ID",
        )(self.delete)

    async def get_all(
        self,
        filter: RoleFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[RoleRDTO]:
        use_case = AllRoleCase(db)
        try:
            return await use_case.execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: RoleCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> RoleRDTO:
        use_case = CreateRoleCase(db)
        try:
            return await use_case.execute(dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: RoleCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> RoleRDTO:
        use_case = UpdateRoleCase(db)
        try:
            return await use_case.execute(id=id, dto=dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> RoleRDTO:
        use_case = GetRoleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get_by_value(
        self,
        value: RoutePathConstants.ValuePath,
        db: AsyncSession = Depends(get_db),
    ) -> RoleRDTO:
        use_case = GetRoleByValueCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        use_case = DeleteRoleByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc
