from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import (
    CartRDTO,
    CartCDTO,
    PaginationCartRDTO,
    CartUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.cart.cart_filter import CartFilter
from app.adapters.filters.cart.cart_pagination_filter import CartPaginationFilter
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.cart.all_carts_case import AllCartsCase
from app.use_case.cart.create_cart_case import CreateCartCase
from app.use_case.cart.delete_cart_case import DeleteCartCase
from app.use_case.cart.get_cart_by_id_case import GetCartByIdCase
from app.use_case.cart.get_cart_by_user_id_case import GetCartByUserIdCase
from app.use_case.cart.paginate_carts_case import PaginateCartsCase
from app.use_case.cart.update_cart_case import UpdateCartCase


class CartApi:
    def __init__(self) -> None:
        """
        Инициализация CartApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API корзин.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationCartRDTO,
            summary="Список корзин с пагинацией",
            description="Получение списка корзин с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[CartRDTO],
            summary="Список всех корзин",
            description="Получение полного списка корзин",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=CartRDTO,
            summary="Создать корзину",
            description="Создание новой корзины для пользователя",
        )(self.create)

        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=CartRDTO,
            summary="Обновить корзину по ID",
            description="Обновление информации о корзине по её ID",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=CartRDTO,
            summary="Получить корзину по ID",
            description="Получение информации о корзине по ID",
        )(self.get_by_id)

        self.router.get(
            "/get-by-user/{user_id}",
            response_model=CartRDTO,
            summary="Получить корзину пользователя",
            description="Получение корзины конкретного пользователя",
        )(self.get_by_user_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить корзину по ID",
            description="Удаление корзины по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: CartPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationCartRDTO:
        try:
            return await PaginateCartsCase(db).execute(filter)
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
        filter: CartFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[CartRDTO]:
        try:
            return await AllCartsCase(db).execute(filter)
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
        dto: CartCDTO = Depends(FormParserHelper.parse_cart_dto_from_form),
        db: AsyncSession = Depends(get_db),
    ) -> CartRDTO:
        try:
            return await CreateCartCase(db).execute(dto=dto)
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
        dto: CartUpdateDTO = Depends(FormParserHelper.parse_cart_update_dto_from_form),
        db: AsyncSession = Depends(get_db),
    ) -> CartRDTO:
        try:
            return await UpdateCartCase(db).execute(id=id, dto=dto)
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
    ) -> CartRDTO:
        try:
            return await GetCartByIdCase(db).execute(id=id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_by_user_id(
        self,
        user_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
    ) -> CartRDTO:
        try:
            return await GetCartByUserIdCase(db).execute(user_id=user_id)
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
            return await DeleteCartCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc