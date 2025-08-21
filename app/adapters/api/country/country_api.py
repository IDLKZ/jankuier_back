from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.country.country_dto import CountryRDTO, CountryCDTO
from app.adapters.dto.pagination_dto import PaginationCountryRDTO
from app.adapters.filters.country.country_filter import CountryFilter
from app.adapters.filters.country.country_pagination_filter import (
    CountryPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.country.all_country_case import AllCountryCase
from app.use_case.country.create_country_case import CreateCountryCase
from app.use_case.country.delete_country_case import DeleteCountryByIdCase
from app.use_case.country.get_country_by_id_case import GetCountryByIdCase
from app.use_case.country.paginate_country_case import PaginateCountryCase
from app.use_case.country.update_country_case import UpdateCountryCase


class CountryApi:
    def __init__(self) -> None:
        """
        Инициализация CountryApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API стран.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationCountryRDTO,
            summary="Список стран с пагинацией",
            description="Получение списка стран с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[CountryRDTO],
            summary="Список всех стран",
            description="Получение полного списка стран",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=CountryRDTO,
            summary="Создать страну",
            description="Создание новой страны",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=CountryRDTO,
            summary="Обновить страну по ID",
            description="Обновление информации о стране по её ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=CountryRDTO,
            summary="Получить страну по ID",
            description="Получение информации о стране по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить страну по ID",
            description="Удаление страны по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: CountryPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationCountryRDTO:
        try:
            return await PaginateCountryCase(db).execute(filter)
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
        filter: CountryFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[CountryRDTO]:
        try:
            return await AllCountryCase(db).execute(filter)
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
        dto: CountryCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CountryRDTO:
        try:
            return await CreateCountryCase(db).execute(dto=dto)
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
        dto: CountryCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CountryRDTO:
        try:
            return await UpdateCountryCase(db).execute(id=id, dto=dto)
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
    ) -> CountryRDTO:
        try:
            return await GetCountryByIdCase(db).execute(id=id)
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
            return await DeleteCountryByIdCase(db).execute(
                id=id, force_delete=force_delete
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc
