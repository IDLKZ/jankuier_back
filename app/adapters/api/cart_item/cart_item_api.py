from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart_item.cart_item_dto import (
    CartItemWithRelationsRDTO,
    CartItemCDTO,
    PaginationCartItemWithRelationsRDTO,
    CartItemUpdateDTO,
)
from app.helpers.form_helper import FormParserHelper
from app.adapters.filters.cart_item.cart_item_filter import CartItemFilter
from app.adapters.filters.cart_item.cart_item_pagination_filter import (
    CartItemPaginationFilter,
)
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.shared.query_constants import AppQueryConstants
from app.shared.route_constants import RoutePathConstants
from app.use_case.cart_item.all_cart_items_case import AllCartItemsCase
from app.use_case.cart_item.create_cart_item_case import CreateCartItemCase
from app.use_case.cart_item.delete_cart_item_case import DeleteCartItemCase
from app.use_case.cart_item.get_cart_item_by_id_case import GetCartItemByIdCase
from app.use_case.cart_item.paginate_cart_items_case import PaginateCartItemsCase
from app.use_case.cart_item.update_cart_item_case import UpdateCartItemCase


class CartItemApi:
    def __init__(self) -> None:
        """
        Инициализация CartItemApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API товаров в корзине.
        """
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.get(
            RoutePathConstants.IndexPathName,
            response_model=PaginationCartItemWithRelationsRDTO,
            summary="Список товаров в корзинах с пагинацией",
            description="Получение списка товаров в корзинах с постраничной фильтрацией",
        )(self.paginate)

        self.router.get(
            RoutePathConstants.AllPathName,
            response_model=list[CartItemWithRelationsRDTO],
            summary="Список всех товаров в корзинах",
            description="Получение полного списка товаров в корзинах",
        )(self.get_all)

        self.router.post(
            RoutePathConstants.CreatePathName,
            response_model=CartItemWithRelationsRDTO,
            summary="Добавить товар в корзину",
            description="Добавление товара в корзину с расчетом цен",
        )(self.create)


        self.router.put(
            RoutePathConstants.UpdatePathName,
            response_model=CartItemWithRelationsRDTO,
            summary="Обновить товар в корзине по ID",
            description="Обновление количества или цены товара в корзине",
        )(self.update)

        self.router.get(
            RoutePathConstants.GetByIdPathName,
            response_model=CartItemWithRelationsRDTO,
            summary="Получить товар в корзине по ID",
            description="Получение информации о товаре в корзине по ID",
        )(self.get_by_id)

        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить товар из корзины по ID",
            description="Удаление товара из корзины по ID",
        )(self.delete)

    async def paginate(
        self,
        filter: CartItemPaginationFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> PaginationCartItemWithRelationsRDTO:
        try:
            return await PaginateCartItemsCase(db).execute(filter)
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
        filter: CartItemFilter = Depends(),
        db: AsyncSession = Depends(get_db),
    ) -> list[CartItemWithRelationsRDTO]:
        try:
            return await AllCartItemsCase(db).execute(filter)
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
        dto: CartItemCDTO = Depends(FormParserHelper.parse_cart_item_dto_from_form),
        db: AsyncSession = Depends(get_db),
    ) -> CartItemWithRelationsRDTO:
        try:
            return await CreateCartItemCase(db).execute(dto=dto)
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
        dto: CartItemUpdateDTO = Depends(
            FormParserHelper.parse_cart_item_update_dto_from_form
        ),
        db: AsyncSession = Depends(get_db),
    ) -> CartItemWithRelationsRDTO:
        try:
            return await UpdateCartItemCase(db).execute(id=id, dto=dto)
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
    ) -> CartItemWithRelationsRDTO:
        try:
            return await GetCartItemByIdCase(db).execute(id=id)
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
            return await DeleteCartItemCase(db).execute(id=id, force_delete=force_delete)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc