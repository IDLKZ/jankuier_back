from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.category_modification.category_modification_dto import (
    CategoryModificationWithRelationsRDTO,
    CategoryModificationCDTO,
)
from app.adapters.dto.pagination_dto import PaginationCategoryModificationWithRelationsRDTO
from app.adapters.filters.category_modification.category_modification_filter import (
    CategoryModificationFilter,
)
from app.adapters.filters.category_modification.category_modification_pagination_filter import (
    CategoryModificationPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.category_modification.all_category_modification_case import (
    AllCategoryModificationCase,
)
from app.use_case.category_modification.create_category_modification_case import (
    CreateCategoryModificationCase,
)
from app.use_case.category_modification.delete_category_modification_case import (
    DeleteCategoryModificationCase,
)
from app.use_case.category_modification.get_category_modification_by_id_case import (
    GetCategoryModificationByIdCase,
)
from app.use_case.category_modification.paginate_category_modification_case import (
    PaginateCategoryModificationCase,
)
from app.use_case.category_modification.update_category_modification_case import (
    UpdateCategoryModificationCase,
)


class CategoryModificationApi:
    def __init__(self) -> None:
        """
        Инициализация CategoryModificationApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API модификаций категорий.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationCategoryModificationWithRelationsRDTO,
            summary="Список модификаций категорий с пагинацией",
            description="Получение списка модификаций категорий с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[CategoryModificationWithRelationsRDTO],
            summary="Список всех модификаций категорий",
            description="Получение полного списка модификаций категорий",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=CategoryModificationWithRelationsRDTO,
            summary="Создать модификацию категории",
            description="Создание новой модификации категории",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=CategoryModificationWithRelationsRDTO,
            summary="Обновить модификацию категории по ID",
            description="Обновление информации о модификации категории по его ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=CategoryModificationWithRelationsRDTO,
            summary="Получить модификацию категории по ID",
            description="Получение информации о модификации категории по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить модификацию категории по ID",
            description="Удаление модификации категории по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: CategoryModificationPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationCategoryModificationWithRelationsRDTO:
        try:
            return await PaginateCategoryModificationCase(db).execute(filter)
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
        filter: CategoryModificationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[CategoryModificationWithRelationsRDTO]:
        try:
            return await AllCategoryModificationCase(db).execute(filter)
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
        dto: CategoryModificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CategoryModificationWithRelationsRDTO:
        try:
            return await CreateCategoryModificationCase(db).execute(dto=dto)
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
        dto: CategoryModificationCDTO,
        db: AsyncSession = Depends(get_db),
    ) -> CategoryModificationWithRelationsRDTO:
        try:
            return await UpdateCategoryModificationCase(db).execute(id=id, dto=dto)
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
    ) -> CategoryModificationWithRelationsRDTO:
        try:
            return await GetCategoryModificationByIdCase(db).execute(id=id)
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
            return await DeleteCategoryModificationCase(db).execute(
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