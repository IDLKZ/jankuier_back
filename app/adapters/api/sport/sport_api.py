from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.sport.sport_dto import SportRDTO, SportCDTO
from app.adapters.dto.pagination_dto import PaginationSportRDTO
from app.adapters.filters.sport.sport_filter import SportFilter
from app.adapters.filters.sport.sport_pagination_filter import SportPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.sport.all_sport_case import AllSportCase
from app.use_case.sport.create_sport_case import CreateSportCase
from app.use_case.sport.delete_sport_case import DeleteSportCase
from app.use_case.sport.get_sport_by_id_case import GetSportByIdCase
from app.use_case.sport.get_sport_by_value_case import GetSportByValueCase
from app.use_case.sport.paginate_sport_case import PaginateSportCase
from app.use_case.sport.update_sport_case import UpdateSportCase


class SportApi:
    def __init__(self) -> None:
        """
        Инициализация SportApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API видов спорта.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationSportRDTO,
            summary="Список видов спорта с пагинацией",
            description="Получение списка видов спорта с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[SportRDTO],
            summary="Список всех видов спорта",
            description="Получение полного списка видов спорта",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=SportRDTO,
            summary="Создать вид спорта",
            description="Создание нового вида спорта",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=SportRDTO,
            summary="Обновить вид спорта по ID",
            description="Обновление информации о виде спорта по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=SportRDTO,
            summary="Получить вид спорта по ID",
            description="Получение информации о виде спорта по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=SportRDTO,
            summary="Получить вид спорта по значению",
            description="Получение информации о виде спорта по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить вид спорта по ID",
            description="Удаление вида спорта по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: SportPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationSportRDTO:
        try:
            return await PaginateSportCase(db).execute(filter)
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
        filter: SportFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[SportRDTO]:
        try:
            return await AllSportCase(db).execute(filter)
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
        dto: SportCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> SportRDTO:
        try:
            return await CreateSportCase(db).execute(dto=dto)
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
        dto: SportCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> SportRDTO:
        try:
            return await UpdateSportCase(db).execute(id=id, dto=dto)
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
    ) -> SportRDTO:
        try:
            return await GetSportByIdCase(db).execute(id=id)
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
    ) -> SportRDTO:
        try:
            return await GetSportByValueCase(db).execute(value=value)
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
            return await DeleteSportCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
