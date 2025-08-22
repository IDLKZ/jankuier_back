from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party.field_party_dto import FieldPartyWithRelationsRDTO, FieldPartyCDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationFieldPartyWithRelationsRDTO
from app.adapters.filters.field_party.field_party_filter import FieldPartyFilter
from app.adapters.filters.field_party.field_party_pagination_filter import (
    FieldPartyPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.field_party.all_field_party_case import AllFieldPartyCase
from app.use_case.field_party.create_field_party_case import CreateFieldPartyCase
from app.use_case.field_party.delete_field_party_case import DeleteFieldPartyByIdCase
from app.use_case.field_party.get_field_party_by_id_case import GetFieldPartyByIdCase
from app.use_case.field_party.get_field_party_by_value_case import GetFieldPartyByValueCase
from app.use_case.field_party.paginate_field_party_case import PaginateFieldPartyCase
from app.use_case.field_party.update_field_party_case import UpdateFieldPartyCase


class FieldPartyApi:
    def __init__(self) -> None:
        """
        Инициализация FieldPartyApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API площадок полей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFieldPartyWithRelationsRDTO,
            summary="Список площадок полей с пагинацией",
            description="Получение списка площадок полей с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[FieldPartyWithRelationsRDTO],
            summary="Список всех площадок полей",
            description="Получение полного списка площадок полей",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FieldPartyWithRelationsRDTO,
            summary="Создать площадку поля",
            description="Создание новой площадки поля",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FieldPartyWithRelationsRDTO,
            summary="Обновить площадку поля по ID",
            description="Обновление информации о площадке поля по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FieldPartyWithRelationsRDTO,
            summary="Получить площадку поля по ID",
            description="Получение информации о площадке поля по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=FieldPartyWithRelationsRDTO,
            summary="Получить площадку поля по значению",
            description="Получение информации о площадке поля по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить площадку поля по ID",
            description="Удаление площадки поля по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: FieldPartyPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFieldPartyWithRelationsRDTO:
        try:
            return await PaginateFieldPartyCase(db).execute(filter)
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
        filter: FieldPartyFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[FieldPartyWithRelationsRDTO]:
        try:
            return await AllFieldPartyCase(db).execute(filter)
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
        dto: FieldPartyCDTO = Depends(FormParserHelper.parse_field_party_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyWithRelationsRDTO:
        try:
            return await CreateFieldPartyCase(db).execute(dto=dto, file=file)
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
        dto: FieldPartyCDTO = Depends(FormParserHelper.parse_field_party_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyWithRelationsRDTO:
        try:
            return await UpdateFieldPartyCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> FieldPartyWithRelationsRDTO:
        try:
            return await GetFieldPartyByIdCase(db).execute(id=id)
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
    ) -> FieldPartyWithRelationsRDTO:
        try:
            return await GetFieldPartyByValueCase(db).execute(value=value)
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
            return await DeleteFieldPartyByIdCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc