from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.adapters.dto.cart.cart_dto import CartWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.db import get_db
from app.shared.route_constants import RoutePathConstants
from app.use_case.cart.add_to_cart_case import AddToCartCase
from app.use_case.cart.clear_cart_case import ClearCartCase
from app.use_case.cart.get_user_cart_case import GetUserCartCase
from app.use_case.cart.remove_from_cart_case import RemoveFromCartCase


class AddToCartDTO(BaseModel):
    """DTO для добавления товара в корзину"""
    product_id: int = Field(..., gt=0, description="ID товара")
    qty: int = Field(default=1, gt=0, description="Количество товара")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")


class RemoveFromCartDTO(BaseModel):
    """DTO для удаления товара из корзины"""
    product_id: int = Field(..., gt=0, description="ID товара")
    qty_to_remove: int | None = Field(default=None, gt=0, description="Количество для удаления (если не указано - удаляет полностью)")
    variant_id: int | None = Field(default=None, gt=0, description="ID варианта товара (опционально)")
    remove_completely: bool = Field(default=False, description="Флаг полного удаления товара")


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
            "/get/{user_id}",
            response_model=CartWithRelationsRDTO | None,
            summary="Получить корзину пользователя",
            description="Получает корзину пользователя с автоматическим созданием, если её нет"
        )(self.get_user_cart)
        
        self.router.post(
            "/add/{user_id}",
            response_model=CartWithRelationsRDTO,
            summary="Добавить товар в корзину",
            description="Добавляет товар в корзину пользователя"
        )(self.add_to_cart)
        
        self.router.post(
            "/remove/{user_id}",
            response_model=CartWithRelationsRDTO,
            summary="Удалить товар из корзины",
            description="Удаляет товар из корзины пользователя"
        )(self.remove_from_cart)
        
        self.router.delete(
            "/clear/{user_id}",
            response_model=CartWithRelationsRDTO,
            summary="Очистить корзину",
            description="Удаляет все товары из корзины пользователя"
        )(self.clear_cart)

    async def get_user_cart(
        self,
        user_id: RoutePathConstants.IDPath,
        create_if_not_exists: bool = Query(default=True, description="Создать корзину, если её нет"),
        db: AsyncSession = Depends(get_db),
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
                user_id=user_id,
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
        user_id: RoutePathConstants.IDPath,
        dto: AddToCartDTO,
        db: AsyncSession = Depends(get_db),
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
                user_id=user_id,
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
        user_id: RoutePathConstants.IDPath,
        dto: RemoveFromCartDTO,
        db: AsyncSession = Depends(get_db),
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
                user_id=user_id,
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
        user_id: RoutePathConstants.IDPath,
        db: AsyncSession = Depends(get_db),
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
            return await ClearCartCase(db).execute(user_id=user_id)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc