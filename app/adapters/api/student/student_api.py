from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.student.student_dto import (
    StudentWithRelationsRDTO,
    StudentCDTO,
    PaginationStudentWithRelationsRDTO,
    StudentUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.student.student_filter import StudentFilter
from app.adapters.filters.student.student_pagination_filter import (
    StudentPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.student.all_student_case import AllStudentCase
from app.use_case.student.create_student_case import CreateStudentCase
from app.use_case.student.delete_student_case import DeleteStudentCase
from app.use_case.student.get_student_by_id_case import GetStudentByIdCase
from app.use_case.student.paginate_student_case import PaginateStudentCase
from app.use_case.student.update_student_case import UpdateStudentCase


class StudentApi:
    def __init__(self) -> None:
        """
        Инициализация StudentApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API студентов.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationStudentWithRelationsRDTO,
            summary="Список студентов с пагинацией",
            description="Получение списка студентов с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[StudentWithRelationsRDTO],
            summary="Список всех студентов",
            description="Получение полного списка студентов",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=StudentWithRelationsRDTO,
            summary="Создать студента",
            description="Создание нового студента",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=StudentWithRelationsRDTO,
            summary="Обновить студента по ID",
            description="Обновление информации о студенте по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=StudentWithRelationsRDTO,
            summary="Получить студента по ID",
            description="Получение информации о студенте по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить студента по ID",
            description="Удаление студента по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: StudentPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationStudentWithRelationsRDTO:
        try:
            return await PaginateStudentCase(db).execute(filter)
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
        filter: StudentFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[StudentWithRelationsRDTO]:
        try:
            return await AllStudentCase(db).execute(filter)
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
        dto: StudentCDTO = Depends(FormParserHelper.parse_student_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> StudentWithRelationsRDTO:
        try:
            return await CreateStudentCase(db).execute(dto=dto, file=file)
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
        dto: StudentUpdateDTO = Depends(FormParserHelper.parse_student_update_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> StudentWithRelationsRDTO:
        try:
            return await UpdateStudentCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> StudentWithRelationsRDTO:
        try:
            return await GetStudentByIdCase(db).execute(id=id)
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
            return await DeleteStudentCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc