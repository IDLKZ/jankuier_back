from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_type.modification_type_dto import (
    ModificationTypeRDTO,
    ModificationTypeCDTO,
)
from app.adapters.dto.pagination_dto import PaginationModificationTypeRDTO
from app.adapters.filters.modification_type.modification_type_filter import (
    ModificationTypeFilter,
)
from app.adapters.filters.modification_type.modification_type_pagination_filter import (
    ModificationTypePaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.modification_type.all_modification_type_case import (
    AllModificationTypeCase,
)
from app.use_case.modification_type.create_modification_type_case import (
    CreateModificationTypeCase,
)
from app.use_case.modification_type.delete_modification_type_case import (
    DeleteModificationTypeCase,
)
from app.use_case.modification_type.get_modification_type_by_id_case import (
    GetModificationTypeByIdCase,
)
from app.use_case.modification_type.get_modification_type_by_value_case import (
    GetModificationTypeByValueCase,
)
from app.use_case.modification_type.paginate_modification_type_case import (
    PaginateModificationTypeCase,
)
from app.use_case.modification_type.update_modification_type_case import (
    UpdateModificationTypeCase,
)


class ModificationTypeApi:
    def __init__(self) -> None:
        """
        Инициализация ModificationTypeApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API типов модификаций.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationModificationTypeRDTO,
            summary="Список типов модификаций с пагинацией",
            description="Получение списка типов модификаций с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ModificationTypeRDTO],
            summary="Список всех типов модификаций",
            description="Получение полного списка типов модификаций",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ModificationTypeRDTO,
            summary="Создать тип модификации",
            description="Создание нового типа модификации",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ModificationTypeRDTO,
            summary="Обновить тип модификации по ID",
            description="Обновление информации о типе модификации по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ModificationTypeRDTO,
            summary="Получить тип модификации по ID",
            description="Получение информации о типе модификации по ID",
        )(self.get_by_id)

        self.router.get(
            RoutePathConstants.GetByValuePathName,
            response_model=ModificationTypeRDTO,
            summary="Получить тип модификации по значению",
            description="Получение информации о типе модификации по уникальному значению (value)",
        )(self.get_by_value)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить тип модификации по ID",
            description="Удаление типа модификации по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ModificationTypePaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationModificationTypeRDTO:
        try:
            return await PaginateModificationTypeCase(db).execute(filter)
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
        filter: ModificationTypeFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ModificationTypeRDTO]:
        try:
            return await AllModificationTypeCase(db).execute(filter)
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
        dto: ModificationTypeCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ModificationTypeRDTO:
        try:
            return await CreateModificationTypeCase(db).execute(dto=dto)
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
        dto: ModificationTypeCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ModificationTypeRDTO:
        try:
            return await UpdateModificationTypeCase(db).execute(id=id, dto=dto)
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
    ) -> ModificationTypeRDTO:
        try:
            return await GetModificationTypeByIdCase(db).execute(id=id)
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
    ) -> ModificationTypeRDTO:
        try:
            return await GetModificationTypeByValueCase(db).execute(value=value)
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
            return await DeleteModificationTypeCase(db).execute(
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
