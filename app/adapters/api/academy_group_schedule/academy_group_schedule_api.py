from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import (
    AcademyGroupScheduleWithRelationsRDTO,
    AcademyGroupScheduleCDTO,
    PaginationAcademyGroupScheduleWithRelationsRDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.academy_group_schedule.academy_group_schedule_filter import (
    AcademyGroupScheduleFilter,
)
from app.adapters.filters.academy_group_schedule.academy_group_schedule_pagination_filter import (
    AcademyGroupSchedulePaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy_group_schedule.all_academy_group_schedules_case import (
    AllAcademyGroupSchedulesCase,
)
from app.use_case.academy_group_schedule.create_academy_group_schedule_case import (
    CreateAcademyGroupScheduleCase,
)
from app.use_case.academy_group_schedule.delete_academy_group_schedule_case import (
    DeleteAcademyGroupScheduleCase,
)
from app.use_case.academy_group_schedule.get_academy_group_schedule_by_id_case import (
    GetAcademyGroupScheduleByIdCase,
)
from app.use_case.academy_group_schedule.paginate_academy_group_schedules_case import (
    PaginateAcademyGroupSchedulesCase,
)
from app.use_case.academy_group_schedule.update_academy_group_schedule_case import (
    UpdateAcademyGroupScheduleCase,
)
from app.use_case.academy_group_schedule.get_academy_group_schedule_by_day_and_group_case import (
    GetAcademyGroupScheduleByDayAndGroupUseCase,
)


class AcademyGroupScheduleApi:
    def __init__(self) -> None:
        """
        Инициализация AcademyGroupScheduleApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API расписаний групп академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyGroupScheduleWithRelationsRDTO,
            summary="Список расписаний групп академий с пагинацией",
            description="Получение списка расписаний групп академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyGroupScheduleWithRelationsRDTO],
            summary="Список всех расписаний групп академий",
            description="Получение полного списка расписаний групп академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyGroupScheduleWithRelationsRDTO,
            summary="Создать расписание группы академии",
            description="Создание нового расписания группы академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyGroupScheduleWithRelationsRDTO,
            summary="Обновить расписание группы академии по ID",
            description="Обновление расписания группы академии по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyGroupScheduleWithRelationsRDTO,
            summary="Получить расписание группы академии по ID",
            description="Получение расписания группы академии по ID",
        )(self.get_by_id)

        self.router.get(
            "/get-by-day-and-groups",
            response_model=list[AcademyGroupScheduleWithRelationsRDTO],
            summary="Получить расписание по дню и группам",
            description="Получение расписания групп академии по конкретной дате и списку ID групп",
        )(self.get_by_day_and_groups)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить расписание группы академии по ID",
            description="Удаление расписания группы академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyGroupSchedulePaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyGroupScheduleWithRelationsRDTO:
        try:
            return await PaginateAcademyGroupSchedulesCase(db).execute(filter)
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
        filter: AcademyGroupScheduleFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyGroupScheduleWithRelationsRDTO]:
        try:
            return await AllAcademyGroupSchedulesCase(db).execute(filter)
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
        dto: AcademyGroupScheduleCDTO = Depends(
            FormParserHelper.parse_academy_group_schedule_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupScheduleWithRelationsRDTO:
        try:
            return await CreateAcademyGroupScheduleCase(db).execute(dto=dto)
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
        dto: AcademyGroupScheduleCDTO = Depends(
            FormParserHelper.parse_academy_group_schedule_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupScheduleWithRelationsRDTO:
        try:
            return await UpdateAcademyGroupScheduleCase(db).execute(id=id, dto=dto)
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
    ) -> AcademyGroupScheduleWithRelationsRDTO:
        try:
            return await GetAcademyGroupScheduleByIdCase(db).execute(id=id)
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
            return await DeleteAcademyGroupScheduleCase(db).execute(
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

    async def get_by_day_and_groups(
        self,
        day: date = Query(..., description="Дата тренировки в формате YYYY-MM-DD"),
        group_ids: list[int] = Query(..., description="Список ID групп академии"),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyGroupScheduleWithRelationsRDTO]:
        try:
            return await GetAcademyGroupScheduleByDayAndGroupUseCase(db).execute(
                day=day, group_ids=group_ids
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc