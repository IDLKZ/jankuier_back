from typing import Any

from app.adapters.dto.ticketon.ticketon_show_level_dto import TicketonShowLevelDTO
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase


class GetTicketonShowLevelCase(BaseUseCase[TicketonShowLevelDTO]):
    """
    Use Case для получения данных уровня зала для конкретного сеанса через Ticketon API
    """

    def __init__(self):
        self.ticketon_service = TicketonServiceAPI()

    async def execute(self, *args: Any, **kwargs: Any) -> TicketonShowLevelDTO:
        """
        Основная логика получения данных уровня для сеанса
        """
        await self.validate(*args, **kwargs)
        await self.transform(*args, **kwargs)

        show_id = kwargs.get("show_id")
        level_id = kwargs.get("level_id")
        
        try:
            return await self.ticketon_service.get_ticketon_show_level(
                show_id=show_id, 
                level_id=level_id
            )
        except Exception as exc:
            raise AppExceptionResponse.internal_error(
                message=f"{i18n.gettext('ticketon_show_level_fetch_error')}: {str(exc)}",
                extra={"show_id": show_id, "level_id": level_id},
                is_custom=True,
            ) from exc

    async def validate(self, *args: Any, **kwargs: Any):
        """
        Валидация входных параметров
        """
        show_id = kwargs.get("show_id")
        level_id = kwargs.get("level_id")
        
        if not show_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_show_id_required"),
                is_custom=True,
            )
        
        if not level_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_level_id_required"),
                is_custom=True,
            )
        
        if not isinstance(show_id, int) or show_id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_show_id"),
                extra={"show_id": show_id},
                is_custom=True,
            )
        
        if not isinstance(level_id, int) or level_id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_level_id"),
                extra={"level_id": level_id},
                is_custom=True,
            )

    async def transform(self, *args: Any, **kwargs: Any):
        """
        Преобразование входных данных (в данном случае не требуется)
        """
        pass