from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
    RequestToAcademyGroupWithRelationsRDTO,
    RequestToAcademyGroupCDTO,
    PaginationRequestToAcademyGroupWithRelationsRDTO,
    RequestToAcademyGroupUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.request_to_academy_group.request_to_academy_group_filter import (
    RequestToAcademyGroupFilter,
)
from app.adapters.filters.request_to_academy_group.request_to_academy_group_pagination_filter import (
    RequestToAcademyGroupPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.request_to_academy_group.all_request_to_academy_group_case import (
    AllRequestToAcademyGroupCase,
)
from app.use_case.request_to_academy_group.create_request_to_academy_group_case import (
    CreateRequestToAcademyGroupCase,
)
from app.use_case.request_to_academy_group.delete_request_to_academy_group_case import (
    DeleteRequestToAcademyGroupCase,
)
from app.use_case.request_to_academy_group.get_request_to_academy_group_by_id_case import (
    GetRequestToAcademyGroupByIdCase,
)
from app.use_case.request_to_academy_group.paginate_request_to_academy_group_case import (
    PaginateRequestToAcademyGroupCase,
)
from app.use_case.request_to_academy_group.update_request_to_academy_group_case import (
    UpdateRequestToAcademyGroupCase,
)


class RequestToAcademyGroupApi:
    def __init__(self) -> None:
        """
        Инициализация RequestToAcademyGroupApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API заявок в группы академий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationRequestToAcademyGroupWithRelationsRDTO,
            summary="Список заявок в группы академий с пагинацией",
            description="Получение списка заявок в группы академий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[RequestToAcademyGroupWithRelationsRDTO],
            summary="Список всех заявок в группы академий",
            description="Получение полного списка заявок в группы академий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=RequestToAcademyGroupWithRelationsRDTO,
            summary="Создать заявку в группу академии",
            description="Создание новой заявки в группу академии",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=RequestToAcademyGroupWithRelationsRDTO,
            summary="Обновить заявку в группу академии по ID",
            description="Обновление информации о заявке в группу академии по её ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=RequestToAcademyGroupWithRelationsRDTO,
            summary="Получить заявку в группу академии по ID",
            description="Получение информации о заявке в группу академии по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить заявку в группу академии по ID",
            description="Удаление заявки в группу академии по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: RequestToAcademyGroupPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationRequestToAcademyGroupWithRelationsRDTO:
        try:
            return await PaginateRequestToAcademyGroupCase(db).execute(filter)
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
        filter: RequestToAcademyGroupFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[RequestToAcademyGroupWithRelationsRDTO]:
        try:
            return await AllRequestToAcademyGroupCase(db).execute(filter)
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
        dto: RequestToAcademyGroupCDTO = Depends(
            FormParserHelper.parse_request_to_academy_group_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> RequestToAcademyGroupWithRelationsRDTO:
        try:
            return await CreateRequestToAcademyGroupCase(db).execute(dto=dto)
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
        dto: RequestToAcademyGroupUpdateDTO = Depends(
            FormParserHelper.parse_request_to_academy_group_update_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> RequestToAcademyGroupWithRelationsRDTO:
        try:
            return await UpdateRequestToAcademyGroupCase(db).execute(id=id, dto=dto)
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
    ) -> RequestToAcademyGroupWithRelationsRDTO:
        try:
            return await GetRequestToAcademyGroupByIdCase(db).execute(id=id)
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
            return await DeleteRequestToAcademyGroupCase(db).execute(
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