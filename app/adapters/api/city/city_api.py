from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.city.city_dto import CityWithRelationsRDTO, CityCDTO
from app.adapters.dto.pagination_dto import PaginationCityWithRelationsRDTO
from app.adapters.filters.city.city_filter import CityFilter
from app.adapters.filters.city.city_pagination_filter import CityPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.city.all_city_case import AllCityCase
from app.use_case.city.create_city_case import CreateCityCase
from app.use_case.city.delete_city_case import DeleteCityByIdCase
from app.use_case.city.get_city_by_id_case import GetCityByIdCase
from app.use_case.city.paginate_city_case import PaginateCityCase
from app.use_case.city.update_city_case import UpdateCityCase


class CityApi:
    def __init__(self) -> None:
        """
        Инициализация CityApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API городов.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationCityWithRelationsRDTO,
            summary="Список городов с пагинацией",
            description="Получение списка городов с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[CityWithRelationsRDTO],
            summary="Список всех городов",
            description="Получение полного списка городов",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=CityWithRelationsRDTO,
            summary="Создать город",
            description="Создание нового города",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=CityWithRelationsRDTO,
            summary="Обновить город по ID",
            description="Обновление информации о городе по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=CityWithRelationsRDTO,
            summary="Получить город по ID",
            description="Получение информации о городе по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить город по ID",
            description="Удаление города по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: CityPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationCityWithRelationsRDTO:
        try:
            return await PaginateCityCase(db).execute(filter)
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
        filter: CityFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[CityWithRelationsRDTO]:
        try:
            return await AllCityCase(db).execute(filter)
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
        dto: CityCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CityWithRelationsRDTO:
        try:
            return await CreateCityCase(db).execute(dto=dto)
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
        dto: CityCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CityWithRelationsRDTO:
        try:
            return await UpdateCityCase(db).execute(id=id, dto=dto)
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
    ) -> CityWithRelationsRDTO:
        try:
            return await GetCityByIdCase(db).execute(id=id)
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
            return await DeleteCityByIdCase(db).execute(
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
