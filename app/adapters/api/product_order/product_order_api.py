from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.adapters.dto.user.user_dto import UserWithRelationsRDTO
from app.core.app_exception_response import AppExceptionResponse
from app.adapters.dto.product_order_response.product_order_response_dto import ProductOrderResponseDTO
from app.infrastructure.db import get_db
from app.i18n.i18n_wrapper import i18n
from app.middleware.role_middleware import check_client
from app.shared.route_constants import RoutePathConstants
from app.use_case.product_order.client.create_product_order_case import CreateProductOrderCase


class ProductOrderApi:

    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self) -> None:
        self.router.post(
            "create-order-from-cart",
            response_model=ProductOrderResponseDTO,
            summary="Создание заказа из корзины",
            description="Создает заказ на основе содержимого корзины пользователя с интеграцией платежной системы",
        )(self.create_order)

    async def create_order(
        self,
        phone: Optional[str] = Form(None, description="Телефон для заказа (опционально)"),
        email: Optional[str] = Form(None, description="Email для заказа (опционально)"),
        user: UserWithRelationsRDTO = Depends(check_client),
        db: AsyncSession = Depends(get_db),
    ) -> ProductOrderResponseDTO:
        try:
            return await CreateProductOrderCase(db).execute(user=user, phone=phone, email=email)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("internal_server_error"),
                extra={"details": str(exc)},
                is_custom=True,
            ) from exc