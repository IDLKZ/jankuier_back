import traceback

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from app.adapters.dto.user.user_dto import UserCDTO, UserWithRelationsRDTO, UserCDTO, UserUDTO
from app.adapters.dto.pagination_dto import PaginationUserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.helpers.form_helper import FormParserHelper
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.middleware.role_middleware import check_client
from app.shared.route_constants import RoutePathConstants
from app.adapters.filters.user.user_pagination_filter import UserPaginationFilter
from app.adapters.filters.user.user_filter import UserFilter
from app.use_case.auth.deactivate_my_account import DeactivateMyAccount
from app.use_case.user.all_user_case import AllUserCase
from app.use_case.user.create_user_case import CreateUserCase
from app.use_case.user.delete_user_case import DeleteUserByIdCase
from app.use_case.user.get_user_by_id_case import GetUserByIdCase
from app.use_case.user.get_user_by_username_case import GetUserByUsernameCase
from app.use_case.user.paginate_user_case import PaginateUserCase
from app.use_case.user.update_user_case import UpdateUserCase


class UserApi:

    def __init__(self) -> None:
        """
        Инициализация UserApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API ролей.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            f"{RoutePathConstants.IndexPathName}",
            response_model=PaginationUserWithRelationsRDTO,
            summary="Список пользователей",
            description="Получение списка пользователей",
        )(self.paginate)
        self.router.get(
            f"{RoutePathConstants.AllPathName}",
            response_model=list[UserWithRelationsRDTO],
            summary="Список пользователей",
            description="Получение списка пользователей",
        )(self.get_all)
        self.router.post(
            f"{RoutePathConstants.CreatePathName}",
            response_model=UserWithRelationsRDTO,
            summary="Создать пользователя",
            description="Создание пользователя",
        )(self.create)
        self.router.put(
            f"{RoutePathConstants.UpdatePathName}",
            response_model=UserWithRelationsRDTO,
            summary="Обновить пользователя по ID",
            description="Обновление пользователя по ID",
        )(self.update)
        self.router.get(
            f"{RoutePathConstants.GetByIdPathName}",
            response_model=UserWithRelationsRDTO,
            summary="Получить пользователя по ID",
            description="Получение пользователя по ID",
        )(self.get)
        self.router.get(
            f"{RoutePathConstants.GetByValuePathName}",
            response_model=UserWithRelationsRDTO,
            summary="Получить пользователя по уникальному значению",
            description="Получение пользователя по уникальному значению",
        )(self.get_by_value)
        self.router.delete(
            f"{RoutePathConstants.DeleteByIdPathName}",
            response_model=bool,
            summary="Удалите пользователя по ID",
            description="Удаление пользователя по ID",
        )(self.delete)


    async def paginate(
        self,
        filter: UserPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationUserWithRelationsRDTO:
        use_case = PaginateUserCase(db)
        try:
            return await use_case.execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get_all(
        self,
        filter: UserFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[UserWithRelationsRDTO]:
        use_case = AllUserCase(db)
        try:
            return await use_case.execute(filter)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def create(
        self,
        dto: UserCDTO = Depends(FormParserHelper.parse_user_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        use_case = CreateUserCase(db)
        try:
            return await use_case.execute(dto=dto, file=file)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def update(
        self,
        id: RoutePathConstants.IDPath,
        dto: UserUDTO = Depends(FormParserHelper.parse_update_user_dto_from_form),
        file: UploadFile | None = File(default=None),
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        use_case = UpdateUserCase(db)
        try:
            return await use_case.execute(id=id, dto=dto, file=file)
        except HTTPException:
            raise
        except Exception as exc:
            traceback.print_exc()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        use_case = GetUserByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def get_by_value(
        self,
        value: RoutePathConstants.ValuePath,
        db: AsyncSession = Depends(get_db),
    ) -> UserWithRelationsRDTO:
        use_case = GetUserByUsernameCase(db)
        try:
            return await use_case.execute(value=value)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc

    async def delete(
        self,
        id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> bool:
        use_case = DeleteUserByIdCase(db)
        try:
            return await use_case.execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc
