from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_student.academy_group_student_dto import (
    AcademyGroupStudentWithRelationsRDTO,
    AcademyGroupStudentCDTO,
    PaginationAcademyGroupStudentWithRelationsRDTO,
    AcademyGroupStudentUpdateDTO,
    AcademyGroupStudentBulkCDTO,
    AcademyGroupStudentBulkUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.academy_group_student.academy_group_student_filter import (
    AcademyGroupStudentFilter,
)
from app.adapters.filters.academy_group_student.academy_group_student_pagination_filter import (
    AcademyGroupStudentPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.academy_group_student.all_academy_group_student_case import (
    AllAcademyGroupStudentCase,
)
from app.use_case.academy_group_student.create_academy_group_student_case import (
    CreateAcademyGroupStudentCase,
)
from app.use_case.academy_group_student.delete_academy_group_student_case import (
    DeleteAcademyGroupStudentCase,
)
from app.use_case.academy_group_student.get_academy_group_student_by_id_case import (
    GetAcademyGroupStudentByIdCase,
)
from app.use_case.academy_group_student.paginate_academy_group_student_case import (
    PaginateAcademyGroupStudentCase,
)
from app.use_case.academy_group_student.update_academy_group_student_case import (
    UpdateAcademyGroupStudentCase,
)


class AcademyGroupStudentApi:
    def __init__(self) -> None:
        """
        Инициализация AcademyGroupStudentApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API студентов групп академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationAcademyGroupStudentWithRelationsRDTO,
            summary="Список студентов групп академий с пагинацией",
            description="Получение списка студентов групп академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[AcademyGroupStudentWithRelationsRDTO],
            summary="Список всех студентов групп академий",
            description="Получение полного списка студентов групп академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=AcademyGroupStudentWithRelationsRDTO,
            summary="Добавить студента в группу академии",
            description="Добавление студента в группу академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=AcademyGroupStudentWithRelationsRDTO,
            summary="Обновить студента в группе по ID",
            description="Обновление информации о студенте в группе по его ID",
        )(self.update)


        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=AcademyGroupStudentWithRelationsRDTO,
            summary="Получить студента группы по ID",
            description="Получение информации о студенте группы по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить студента из группы по ID",
            description="Удаление студента из группы академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: AcademyGroupStudentPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationAcademyGroupStudentWithRelationsRDTO:
        try:
            return await PaginateAcademyGroupStudentCase(db).execute(filter)
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
        filter: AcademyGroupStudentFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[AcademyGroupStudentWithRelationsRDTO]:
        try:
            return await AllAcademyGroupStudentCase(db).execute(filter)
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
        dto: AcademyGroupStudentCDTO = Depends(
            FormParserHelper.parse_academy_group_student_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupStudentWithRelationsRDTO:
        try:
            return await CreateAcademyGroupStudentCase(db).execute(dto=dto)
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
        dto: AcademyGroupStudentUpdateDTO = Depends(
            FormParserHelper.parse_academy_group_student_update_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> AcademyGroupStudentWithRelationsRDTO:
        try:
            return await UpdateAcademyGroupStudentCase(db).execute(id=id, dto=dto)
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
    ) -> AcademyGroupStudentWithRelationsRDTO:
        try:
            return await GetAcademyGroupStudentByIdCase(db).execute(id=id)
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
            return await DeleteAcademyGroupStudentCase(db).execute(
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