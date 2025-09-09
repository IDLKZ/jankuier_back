from typing import Any

from app.adapters.dto.ticketon.ticketon_get_level_dto import TicketonGetLevelDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase


class GetTicketonLevelCase(BaseUseCase[TicketonGetLevelDTO]):
    """
    Use Case для получения данных уровня зала через Ticketon API
    """

    def __init__(self):
        self.ticketon_service = TicketonServiceAPI()

    async def execute(self, *args: Any, **kwargs: Any) -> TicketonGetLevelDTO:
        """
        Основная логика получения данных уровня
        """
        await self.validate(*args, **kwargs)
        await self.transform(*args, **kwargs)

        level_id = kwargs.get("level_id")
        
        try:
            return await self.ticketon_service.get_ticketon_get_level(level_id=level_id)
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=f"Ошибка получения данных уровня зала: {str(exc)}",
                extra={"level_id": level_id},
                is_custom=True,
            ) from exc

    async def validate(self, *args: Any, **kwargs: Any):
        """
        Валидация входных параметров
        """
        level_id = kwargs.get("level_id")
        
        if not level_id:
            raise AppExceptionResponse.bad_request(
                message="Не указан ID уровня зала",
                is_custom=True,
            )
        
        if not isinstance(level_id, int) or level_id <= 0:
            raise AppExceptionResponse.bad_request(
                message="ID уровня зала должен быть положительным числом",
                extra={"level_id": level_id},
                is_custom=True,
            )

    async def transform(self, *args: Any, **kwargs: Any):
        """
        Преобразование входных данных (в данном случае не требуется)
        """
        pass