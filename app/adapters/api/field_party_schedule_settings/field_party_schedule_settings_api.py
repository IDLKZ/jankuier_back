from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
    FieldPartyScheduleSettingsWithRelationsRDTO,
    FieldPartyScheduleSettingsCDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationFieldPartyScheduleSettingsWithRelationsRDTO
from app.adapters.filters.field_party_schedule_settings.field_party_schedule_settings_filter import (
    FieldPartyScheduleSettingsFilter,
)
from app.adapters.filters.field_party_schedule_settings.field_party_schedule_settings_pagination_filter import (
    FieldPartyScheduleSettingsPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.field_party_schedule_settings.all_field_party_schedule_settings_case import (
    AllFieldPartyScheduleSettingsCase,
)
from app.use_case.field_party_schedule_settings.create_field_party_schedule_settings_case import (
    CreateFieldPartyScheduleSettingsCase,
)
from app.use_case.field_party_schedule_settings.delete_field_party_schedule_settings_case import (
    DeleteFieldPartyScheduleSettingsCase,
)
from app.use_case.field_party_schedule_settings.get_field_party_schedule_settings_by_id_case import (
    GetFieldPartyScheduleSettingsByIdCase,
)
from app.use_case.field_party_schedule_settings.paginate_field_party_schedule_settings_case import (
    PaginateFieldPartyScheduleSettingsCase,
)
from app.use_case.field_party_schedule_settings.update_field_party_schedule_settings_case import (
    UpdateFieldPartyScheduleSettingsCase,
)


class FieldPartyScheduleSettingsApi:
    def __init__(self) -> None:
        """
        Инициализация FieldPartyScheduleSettingsApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API настроек расписания площадок.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFieldPartyScheduleSettingsWithRelationsRDTO,
            summary="Список настроек расписания площадок с пагинацией",
            description="Получение списка настроек расписания площадок с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[FieldPartyScheduleSettingsWithRelationsRDTO],
            summary="Список всех настроек расписания площадок",
            description="Получение полного списка настроек расписания площадок",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FieldPartyScheduleSettingsWithRelationsRDTO,
            summary="Создать настройки расписания площадки",
            description="Создание новых настроек расписания площадки",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FieldPartyScheduleSettingsWithRelationsRDTO,
            summary="Обновить настройки расписания площадки по ID",
            description="Обновление настроек расписания площадки по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FieldPartyScheduleSettingsWithRelationsRDTO,
            summary="Получить настройки расписания площадки по ID",
            description="Получение настроек расписания площадки по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить настройки расписания площадки по ID",
            description="Удаление настроек расписания площадки по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: FieldPartyScheduleSettingsPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFieldPartyScheduleSettingsWithRelationsRDTO:
        try:
            return await PaginateFieldPartyScheduleSettingsCase(db).execute(filter)
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
        filter: FieldPartyScheduleSettingsFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[FieldPartyScheduleSettingsWithRelationsRDTO]:
        try:
            return await AllFieldPartyScheduleSettingsCase(db).execute(filter)
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
        dto: FieldPartyScheduleSettingsCDTO = Depends(
            FormParserHelper.parse_field_party_schedule_settings_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyScheduleSettingsWithRelationsRDTO:
        try:
            return await CreateFieldPartyScheduleSettingsCase(db).execute(dto=dto)
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
        dto: FieldPartyScheduleSettingsCDTO = Depends(
            FormParserHelper.parse_field_party_schedule_settings_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyScheduleSettingsWithRelationsRDTO:
        try:
            return await UpdateFieldPartyScheduleSettingsCase(db).execute(id=id, dto=dto)
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
    ) -> FieldPartyScheduleSettingsWithRelationsRDTO:
        try:
            return await GetFieldPartyScheduleSettingsByIdCase(db).execute(id=id)
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
            return await DeleteFieldPartyScheduleSettingsCase(db).execute(
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