import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.cart.cart_dto import (
    CartRDTO,
    CartCDTO,
    PaginationCartRDTO,
    CartUpdateDTO,
    CartWithRelationsRDTO,
)
from app.adapters.dto.cart.cart_action_dto import AddToCartDTO, UpdateOrRemoveFromCartDTO, CartActionResponseDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
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
from app.use_case.cart.paginate_carts_case import PaginateCartsCase
from app.use_case.cart.update_cart_case import UpdateCartCase
from app.use_case.cart.client.add_to_cart_case import AddToCartCase
from app.use_case.cart.client.update_or_remove_cart_case import UpdateOrRemoveCartCase
from app.use_case.cart.client.clear_cart_case import ClearCartCase
from app.use_case.cart.client.get_user_cart_case import GetUserCartCase
from app.middleware.role_middleware import check_client


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
        self.router.delete(
            RoutePathConstants.DeleteByIdPathName,
            response_model=bool,
            summary="Удалить корзину по ID",
            description="Удаление корзины по ID",
        )(self.delete)

        # Client cart operations
        self.router.post(
            "/add-to-cart",
            response_model=CartActionResponseDTO,
            summary="Добавить товар в корзину",
            description="Добавление товара в корзину пользователя",
        )(self.add_to_cart)

        self.router.put(
            "/update-cart-item",
            response_model=CartActionResponseDTO,
            summary="Обновить/удалить товар в корзине",
            description="Обновление количества или удаление товара из корзины",
        )(self.update_or_remove_cart_item)

        self.router.delete(
            "/clear-cart/{cart_id}",
            response_model=CartActionResponseDTO,
            summary="Очистить корзину",
            description="Полная очистка корзины пользователя",
        )(self.clear_cart)

        self.router.get(
            "/my-cart",
            response_model=CartActionResponseDTO,
            summary="Получить мою корзину",
            description="Получение корзины текущего пользователя с валидацией товаров",
        )(self.get_my_cart)

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


    async def add_to_cart(
        self,
        dto: AddToCartDTO,
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CartActionResponseDTO:
        """
        Добавляет товар в корзину пользователя.

        Args:
            dto: DTO с данными для добавления товара
            user: Аутентифицированный пользователь (клиент)
            db: Сессия базы данных

        Returns:
            CartActionResponseDTO: Ответ с обновленной корзиной
        """
        try:
            return await AddToCartCase(db).execute(dto=dto, user=user)
        except HTTPException:
            raise
        except Exception as exc:
            print(traceback.format_exc())  # полное дерево ошибки
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def update_or_remove_cart_item(
        self,
        dto: UpdateOrRemoveFromCartDTO,
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CartActionResponseDTO:
        """
        Обновляет количество или удаляет товар из корзины.

        Args:
            dto: DTO с данными для обновления/удаления
            user: Аутентифицированный пользователь (клиент)
            db: Сессия базы данных

        Returns:
            CartActionResponseDTO: Ответ с обновленной корзиной
        """
        try:
            return await UpdateOrRemoveCartCase(db).execute(dto=dto, user=user)
        except HTTPException:
            raise
        except Exception as exc:
            print(traceback.format_exc())
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def clear_cart(
        self,
        cart_id: RoutePathConstants.IDPath,
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CartActionResponseDTO:
        """
        Полностью очищает корзину пользователя.

        Args:
            cart_id: ID корзины для очистки
            user: Аутентифицированный пользователь (клиент)
            db: Сессия базы данных

        Returns:
            CartActionResponseDTO: Ответ с очищенной корзиной
        """
        try:
            return await ClearCartCase(db).execute(cart_id=cart_id, user=user)
        except HTTPException:
            raise
        except Exception as exc:
            print(traceback.format_exc())
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def get_my_cart(
        self,
        check_cart_items: bool = False,
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> CartActionResponseDTO:
        """
        Получает корзину текущего пользователя с валидацией товаров.

        Args:
            check_cart_items: Флаг принудительной валидации элементов корзины
            user: Аутентифицированный пользователь (клиент)
            db: Сессия базы данных

        Returns:
            CartActionResponseDTO: Ответ с корзиной пользователя
        """
        try:
            return await GetUserCartCase(db).execute(user=user, check_cart_items=check_cart_items)
        except HTTPException:
            raise
        except Exception as exc:
            print(traceback.format_exc())
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc