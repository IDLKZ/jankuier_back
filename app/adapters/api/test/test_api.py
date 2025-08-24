from fastapi import APIRouter, Depends, HTTPException
from packaging.utils import _
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.db import get_db
from app.infrastructure.service.sota_service.sota_service import SotaService
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.shared.route_constants import RoutePathConstants


class TestApi:

    def __init__(self) -> None:
        """
        Инициализация RoleApi.
        Создаёт объект APIRouter и регистрирует маршруты для взаимодействия с API ролей.
        """
        self.router = APIRouter()
        self._add_routes()


    def _add_routes(self) -> None:
        self.router.get(
            f"{RoutePathConstants.TestGetPathName}",
            summary="Тестовый метод",
            description="Тестовый метод",
        )(self.get_test)


    async def get_test(
        self,
        db: AsyncSession = Depends(get_db),
    ):
        service = TicketonServiceAPI()
        try:
            return await service.get_ticketon_cities()
        except HTTPException:
            raise
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=_("internal_server_error"),
                extra={"details": f"{exc!s}"},
                is_custom=True,
            ) from exc