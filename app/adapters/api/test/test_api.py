from typing import Union, List

from fastapi import APIRouter, Depends, HTTPException
from packaging.utils import _
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.alatau.alatau_cancel_payment_dto import AlatauCancelPaymentDTO
from app.adapters.dto.alatau.alatau_status_request_dto import AlatauStatusRequestDTO
from app.adapters.dto.ticketon.ticketon_booking_dto import TicketonBookingRequestDTO, TicketonBookingErrorResponseDTO, \
    TicketonBookingShowBookingDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.app_config import app_config
from app.infrastructure.db import get_db
from app.infrastructure.service.alatau_service.alatau_service_api import AlatauServiceAPI
from app.infrastructure.service.sota_service.sota_service import SotaService
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.route_constants import RoutePathConstants
from app.adapters.dto.alatau.alatau_cancel_payment_response_dto import AlatauRefundPaymentResultDTO


class TestApi:

    def __init__(self) -> None:
        """
        Инициализация RoleApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API ролей.
        """
        self.router = APIRouter()
        self._add_routes()


    def _add_routes(self) -> None:
        self.router.post(
            f"{RoutePathConstants.TestGetPathName}",
            summary="Тестовый метод",
            description="Тестовый метод",
        )(self.get_test)
        self.router.post(
            f"{RoutePathConstants.TestPostPathName}",
            summary="Тестовый метод",
            description="Тестовый метод",
        )(self.post_test)

    async def get_test(
        self,
        dto:AlatauStatusRequestDTO,
        db: AsyncSession = Depends(get_db),
    ):
        try:
            service = AlatauServiceAPI()
            return await service.get_payment_status(dto)
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc


    async def post_test(
        self,
        dto:TicketonBookingShowBookingDTO,
    ):
        service = TicketonServiceAPI()
        alatau_service = AlatauServiceAPI()
        return await alatau_service.create_for_ticketon_booking(dto)
