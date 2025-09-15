from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.adapters.dto.cart.cart_action_dto import AddToCartDTO, RemoveFromCartDTO
from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.middleware.role_middleware import check_client
from app.shared.route_constants import RoutePathConstants
from app.use_case.cart.add_to_cart_case import AddToCartCase
from app.use_case.cart.clear_cart_case import ClearCartCase
from app.use_case.cart.get_user_cart_case import GetUserCartCase
from app.use_case.cart.remove_from_cart_case import RemoveFromCartCase


class UserCartApi:
    """
    API для управления корзиной пользователя.
    Предоставляет упрощенные методы для работы с корзиной.
    """

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        """Добавляет маршруты для работы с корзиной пользователя"""
        
        self.router.get(
            "/get",
            response_model=CartWithRelationsRDTO | None,
            summary="Получить корзину пользователя",
            description="Получает корзину пользователя с автоматическим созданием, если её нет"
        )(self.get_user_cart)
        
        self.router.post(
            "/add",
            response_model=CartWithRelationsRDTO,
            summary="Добавить товар в корзину",
            description="Добавляет товар в корзину пользователя"
        )(self.add_to_cart)
        
        self.router.post(
            "/remove",
            response_model=CartWithRelationsRDTO,
            summary="Удалить товар из корзины",
            description="Удаляет товар из корзины пользователя"
        )(self.remove_from_cart)
        
        self.router.delete(
            "/clear",
            response_model=CartWithRelationsRDTO,
            summary="Очистить корзину",
            description="Удаляет все товары из корзины пользователя"
        )(self.clear_cart)

    async def get_user_cart(
        self,
        create_if_not_exists: bool = Query(default=True, description="Создать корзину, если её нет"),
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsRDTO = Depends(check_client),
    ) -> CartWithRelationsRDTO | None:
        """
        Получает корзину пользователя.
        
        Args:
            user_id: ID пользователя
            create_if_not_exists: Создать корзину, если её нет
            db: Сессия базы данных
            
        Returns:
            CartWithRelationsRDTO | None: Корзина пользователя или None
        """
        try:
            return await GetUserCartCase(db).execute(
                user_id=user.id,
                create_if_not_exists=create_if_not_exists
            )
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
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsRDTO = Depends(check_client),
    ) -> CartWithRelationsRDTO:
        """
        Добавляет товар в корзину пользователя.
        
        Args:
            user_id: ID пользователя
            dto: Данные товара для добавления
            db: Сессия базы данных
            
        Returns:
            CartWithRelationsRDTO: Обновленная корзина
        """
        try:
            return await AddToCartCase(db).execute(
                user_id=user.id,
                product_id=dto.product_id,
                qty=dto.qty,
                variant_id=dto.variant_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def remove_from_cart(
        self,
        dto: RemoveFromCartDTO,
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsRDTO = Depends(check_client),
    ) -> CartWithRelationsRDTO:
        """
        Удаляет товар из корзины пользователя.
        
        Args:
            user_id: ID пользователя
            dto: Данные товара для удаления
            db: Сессия базы данных
            
        Returns:
            CartWithRelationsRDTO: Обновленная корзина
        """
        try:
            return await RemoveFromCartCase(db).execute(
                user_id=user.id,
                product_id=dto.product_id,
                qty_to_remove=dto.qty_to_remove,
                variant_id=dto.variant_id,
                remove_completely=dto.remove_completely
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc

    async def clear_cart(
        self,
        db: AsyncSession = Depends(get_db),
        user: UserWithRelationsRDTO = Depends(check_client),
    ) -> CartWithRelationsRDTO:
        """
        Очищает корзину пользователя от всех товаров.
        
        Args:
            user_id: ID пользователя
            db: Сессия базы данных
            
        Returns:
            CartWithRelationsRDTO: Пустая корзина
        """
        try:
            return await ClearCartCase(db).execute(user_id=user.id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc