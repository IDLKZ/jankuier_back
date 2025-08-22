from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_material.request_material_dto import (
    RequestMaterialWithRelationsRDTO,
    RequestMaterialCDTO,
    PaginationRequestMaterialWithRelationsRDTO,
    RequestMaterialUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.request_material.request_material_filter import (
    RequestMaterialFilter,
)
from app.adapters.filters.request_material.request_material_pagination_filter import (
    RequestMaterialPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.request_material.all_request_material_case import (
    AllRequestMaterialCase,
)
from app.use_case.request_material.create_request_material_case import (
    CreateRequestMaterialCase,
)
from app.use_case.request_material.delete_request_material_case import (
    DeleteRequestMaterialCase,
)
from app.use_case.request_material.get_request_material_by_id_case import (
    GetRequestMaterialByIdCase,
)
from app.use_case.request_material.paginate_request_material_case import (
    PaginateRequestMaterialCase,
)
from app.use_case.request_material.update_request_material_case import (
    UpdateRequestMaterialCase,
)


class RequestMaterialApi:
    def __init__(self) -> None:
        """
        Инициализация RequestMaterialApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API материалов заявок.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationRequestMaterialWithRelationsRDTO,
            summary="Список материалов заявок с пагинацией",
            description="Получение списка материалов заявок с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[RequestMaterialWithRelationsRDTO],
            summary="Список всех материалов заявок",
            description="Получение полного списка материалов заявок",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=RequestMaterialWithRelationsRDTO,
            summary="Создать материал заявки",
            description="Создание нового материала заявки",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=RequestMaterialWithRelationsRDTO,
            summary="Обновить материал заявки по ID",
            description="Обновление информации о материале заявки по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=RequestMaterialWithRelationsRDTO,
            summary="Получить материал заявки по ID",
            description="Получение информации о материале заявки по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить материал заявки по ID",
            description="Удаление материала заявки по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: RequestMaterialPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationRequestMaterialWithRelationsRDTO:
        try:
            return await PaginateRequestMaterialCase(db).execute(filter)
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
        filter: RequestMaterialFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[RequestMaterialWithRelationsRDTO]:
        try:
            return await AllRequestMaterialCase(db).execute(filter)
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
        dto: RequestMaterialCDTO = Depends(
            FormParserHelper.parse_request_material_dto_from_form
        ),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> RequestMaterialWithRelationsRDTO:
        try:
            return await CreateRequestMaterialCase(db).execute(dto=dto, file=file)
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
        dto: RequestMaterialUpdateDTO = Depends(
            FormParserHelper.parse_request_material_update_dto_from_form
        ),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> RequestMaterialWithRelationsRDTO:
        try:
            return await UpdateRequestMaterialCase(db).execute(id=id, dto=dto, file=file)
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
    ) -> RequestMaterialWithRelationsRDTO:
        try:
            return await GetRequestMaterialByIdCase(db).execute(id=id)
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
            return await DeleteRequestMaterialCase(db).execute(
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