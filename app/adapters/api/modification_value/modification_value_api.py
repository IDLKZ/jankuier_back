from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_value.modification_value_dto import (
    ModificationValueWithRelationsRDTO,
    ModificationValueCDTO,
)
from app.adapters.dto.pagination_dto import PaginationModificationValueWithRelationsRDTO
from app.adapters.filters.modification_value.modification_value_filter import (
    ModificationValueFilter,
)
from app.adapters.filters.modification_value.modification_value_pagination_filter import (
    ModificationValuePaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.modification_value.all_modification_value_case import (
    AllModificationValueCase,
)
from app.use_case.modification_value.create_modification_value_case import (
    CreateModificationValueCase,
)
from app.use_case.modification_value.delete_modification_value_case import (
    DeleteModificationValueCase,
)
from app.use_case.modification_value.get_modification_value_by_id_case import (
    GetModificationValueByIdCase,
)
from app.use_case.modification_value.paginate_modification_value_case import (
    PaginateModificationValueCase,
)
from app.use_case.modification_value.update_modification_value_case import (
    UpdateModificationValueCase,
)


class ModificationValueApi:
    def __init__(self) -> None:
        """
        Инициализация ModificationValueApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API значений модификаций.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationModificationValueWithRelationsRDTO,
            summary="Список значений модификаций с пагинацией",
            description="Получение списка значений модификаций с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[ModificationValueWithRelationsRDTO],
            summary="Список всех значений модификаций",
            description="Получение полного списка значений модификаций",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=ModificationValueWithRelationsRDTO,
            summary="Создать значение модификации",
            description="Создание нового значения модификации",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=ModificationValueWithRelationsRDTO,
            summary="Обновить значение модификации по ID",
            description="Обновление информации о значении модификации по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=ModificationValueWithRelationsRDTO,
            summary="Получить значение модификации по ID",
            description="Получение информации о значении модификации по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить значение модификации по ID",
            description="Удаление значения модификации по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: ModificationValuePaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationModificationValueWithRelationsRDTO:
        try:
            return await PaginateModificationValueCase(db).execute(filter)
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
        filter: ModificationValueFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[ModificationValueWithRelationsRDTO]:
        try:
            return await AllModificationValueCase(db).execute(filter)
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
        dto: ModificationValueCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ModificationValueWithRelationsRDTO:
        try:
            return await CreateModificationValueCase(db).execute(dto=dto)
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
        dto: ModificationValueCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> ModificationValueWithRelationsRDTO:
        try:
            return await UpdateModificationValueCase(db).execute(id=id, dto=dto)
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
    ) -> ModificationValueWithRelationsRDTO:
        try:
            return await GetModificationValueByIdCase(db).execute(id=id)
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
            return await DeleteModificationValueCase(db).execute(
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
