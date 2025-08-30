from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleWithRelationsRDTO,
    FieldPartyScheduleCDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.dto.pagination_dto import PaginationFieldPartyScheduleWithRelationsRDTO
from app.adapters.filters.field_party_schedule.field_party_schedule_filter import (
    FieldPartyScheduleFilter,
)
from app.adapters.filters.field_party_schedule.field_party_schedule_pagination_filter import (
    FieldPartySchedulePaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.field_party_schedule.all_field_party_schedules_case import (
    AllFieldPartySchedulesCase,
)
from app.use_case.field_party_schedule.create_field_party_schedule_case import (
    CreateFieldPartyScheduleCase,
)
from app.use_case.field_party_schedule.delete_field_party_schedule_case import (
    DeleteFieldPartyScheduleCase,
)
from app.use_case.field_party_schedule.get_field_party_schedule_by_id_case import (
    GetFieldPartyScheduleByIdCase,
)
from app.use_case.field_party_schedule.paginate_field_party_schedules_case import (
    PaginateFieldPartySchedulesCase,
)
from app.use_case.field_party_schedule.update_field_party_schedule_case import (
    UpdateFieldPartyScheduleCase,
)
from app.use_case.field_party_schedule.generate_field_party_schedule_case import (
    GenerateFieldPartyScheduleCase,
)
from app.use_case.field_party_schedule.preview_field_party_schedule_case import (
    PreviewFieldPartyScheduleCase,
)
from app.adapters.dto.field_party_schedule_settings.schedule_generator_dto import (
    ScheduleGeneratorResponseDTO,
)


class FieldPartyScheduleApi:
    def __init__(self) -> None:
        """
        Инициализация FieldPartyScheduleApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API расписаний площадок.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationFieldPartyScheduleWithRelationsRDTO,
            summary="Список расписаний площадок с пагинацией",
            description="Получение списка расписаний площадок с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[FieldPartyScheduleWithRelationsRDTO],
            summary="Список всех расписаний площадок",
            description="Получение полного списка расписаний площадок",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=FieldPartyScheduleWithRelationsRDTO,
            summary="Создать расписание площадки",
            description="Создание нового расписания площадки",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=FieldPartyScheduleWithRelationsRDTO,
            summary="Обновить расписание площадки по ID",
            description="Обновление расписания площадки по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=FieldPartyScheduleWithRelationsRDTO,
            summary="Получить расписание площадки по ID",
            description="Получение расписания площадки по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить расписание площадки по ID",
            description="Удаление расписания площадки по ID",
        )(self.delete)

        self.router.post(
            "/generate",
            response_model=ScheduleGeneratorResponseDTO,
            summary="Сгенерировать расписание площадки",
            description="Генерация расписания площадки на основе настроек",
        )(self.generate_schedule)

        self.router.get(
            "/preview",
            response_model=ScheduleGeneratorResponseDTO,
            summary="Предварительный просмотр расписания площадки",
            description="Виртуальная генерация расписания для указанной даты без сохранения в БД",
        )(self.preview_schedule)

    async def paginate(
        self,
        filter: FieldPartySchedulePaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationFieldPartyScheduleWithRelationsRDTO:
        try:
            return await PaginateFieldPartySchedulesCase(db).execute(filter)
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
        filter: FieldPartyScheduleFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[FieldPartyScheduleWithRelationsRDTO]:
        try:
            return await AllFieldPartySchedulesCase(db).execute(filter)
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
        dto: FieldPartyScheduleCDTO = Depends(
            FormParserHelper.parse_field_party_schedule_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyScheduleWithRelationsRDTO:
        try:
            return await CreateFieldPartyScheduleCase(db).execute(dto=dto)
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
        dto: FieldPartyScheduleCDTO = Depends(
            FormParserHelper.parse_field_party_schedule_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> FieldPartyScheduleWithRelationsRDTO:
        try:
            return await UpdateFieldPartyScheduleCase(db).execute(id=id, dto=dto)
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
    ) -> FieldPartyScheduleWithRelationsRDTO:
        try:
            return await GetFieldPartyScheduleByIdCase(db).execute(id=id)
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
            return await DeleteFieldPartyScheduleCase(db).execute(
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

    async def generate_schedule(
        self,
        party_id: int = Query(..., description="ID партии поля для генерации расписания", gt=0),
        regenerate_existing: bool = Query(False, description="Перегенерировать существующие записи расписания"),
        db: AsyncSession = Depends(get_db),
    ) -> ScheduleGeneratorResponseDTO:
        try:
            return await GenerateFieldPartyScheduleCase(db).execute(
                party_id=party_id, regenerate_existing=regenerate_existing
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def preview_schedule(
        self,
        field_party_id: int = Query(..., description="ID партии поля для генерации расписания", gt=0),
        day: str = Query(..., description="Дата для предварительного просмотра в формате YYYY-MM-DD", regex=r"^\d{4}-\d{2}-\d{2}$"),
        db: AsyncSession = Depends(get_db),
    ) -> ScheduleGeneratorResponseDTO:
        try:
            return await PreviewFieldPartyScheduleCase(db).execute(
                field_party_id=field_party_id, day=day
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc