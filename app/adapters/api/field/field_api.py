from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field.field_dto import FieldWithRelationsRDTO, FieldCDTO
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationFieldWithRelationsRDTO
from app.adapters.filters.field.field_filter import FieldFilter
from app.adapters.filters.field.field_pagination_filter import (
    FieldPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.field.all_field_case import AllFieldCase
from app.use_case.field.create_field_case import CreateFieldCase
from app.use_case.field.delete_field_case import DeleteFieldByIdCase
from app.use_case.field.get_field_by_id_case import GetFieldByIdCase
from app.use_case.field.get_field_by_value_case import GetFieldByValueCase
from app.use_case.field.paginate_field_case import PaginateFieldCase
from app.use_case.field.update_field_case import UpdateFieldCase


class FieldApi:
    def __init__(self) -> None:
        """
        Инициализация FieldApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API полей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFieldWithRelationsRDTO,
            summary="Список полей с пагинацией",
            description="Получение списка полей с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[FieldWithRelationsRDTO],
            summary="Список всех полей",
            description="Получение полного списка полей",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FieldWithRelationsRDTO,
            summary="Создать поле",
            description="Создание нового поля",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FieldWithRelationsRDTO,
            summary="Обновить поле по ID",
            description="Обновление информации о поле по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FieldWithRelationsRDTO,
            summary="Получить поле по ID",
            description="Получение информации о поле по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=FieldWithRelationsRDTO,
            summary="Получить поле по значению",
            description="Получение информации о поле по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить поле по ID",
            description="Удаление поля по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: FieldPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFieldWithRelationsRDTO:
        try:
            return await PaginateFieldCase(db).execute(filter)
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
        filter: FieldFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[FieldWithRelationsRDTO]:
        try:
            return await AllFieldCase(db).execute(filter)
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
        dto: FieldCDTO = Depends(FormParserHelper.parse_field_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldWithRelationsRDTO:
        try:
            return await CreateFieldCase(db).execute(dto=dto, file=file)
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
        dto: FieldCDTO = Depends(FormParserHelper.parse_field_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> FieldWithRelationsRDTO:
        try:
            return await UpdateFieldCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> FieldWithRelationsRDTO:
        try:
            return await GetFieldByIdCase(db).execute(id=id)
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
    ) -> FieldWithRelationsRDTO:
        try:
            return await GetFieldByValueCase(db).execute(value=value)
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
            return await DeleteFieldByIdCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc