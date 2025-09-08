from app.adapters.dto.ticketon.ticketon_shows_dto import TicketonShowsDataDTO, TicketonGetShowsParameterDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase
from app.i18n.i18n_wrapper import i18n


class GetTicketonShowsCase(BaseUseCase[TicketonShowsDataDTO]):
    """
    Use Case для получения данных о сеансах Ticketon.
    Получает данные о сеансах через TicketonServiceAPI с кешированием в Redis.
    """

    def __init__(self):
        """
        Инициализация use case для работы с данными Ticketon.
        """
        self.ticketon_service = TicketonServiceAPI()

    async def execute(self, parameter: TicketonGetShowsParameterDTO) -> TicketonShowsDataDTO:
        """
        Основная логика получения данных о сеансах Ticketon.
        
        Args:
            parameter: Параметры запроса (место, тип, язык и т.д.)
            
        Returns:
            TicketonShowsDataDTO: Данные о сеансах, событиях, местах и городах
        """
        await self.validate(parameter)
        await self.transform(parameter)
        
        try:
            return await self.ticketon_service.get_ticketon_shows(parameter)
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("ticketon_shows_fetch_error"),
                extra={"details": str(e)},
                is_custom=True,
            ) from e

    async def validate(self, parameter: TicketonGetShowsParameterDTO):
        """
        Валидация входных параметров для запроса к Ticketon API.
        
        Args:
            parameter: Параметры для валидации
            
        Raises:
            AppExceptionResponse: При некорректных параметрах
        """
        if not parameter:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_parameters_required"),
                is_custom=True,
            )
            
        # Валидация типа события
        if parameter.type and parameter.type not in ["sport"]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_event_type"),
                extra={"allowed_types": ["sport"]},
                is_custom=True,
            )
            
        # Валидация языка
        if parameter.i18n and parameter.i18n not in ["ru", "kk", "en"]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_language"),
                extra={"allowed_languages": ["ru", "kk", "en"]},
                is_custom=True,
            )
            
        # Валидация параметра with
        if parameter.withParam and parameter.withParam not in ["future", "past", "all"]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_with_param"),
                extra={"allowed_values": ["future", "past", "all"]},
                is_custom=True,
            )

    async def transform(self, parameter: TicketonGetShowsParameterDTO):
        """
        Трансформация параметров перед запросом.
        При необходимости можно добавить логику предобработки параметров.
        
        Args:
            parameter: Параметры для трансформации
        """
        # Устанавливаем значения по умолчанию если они не указаны
        if not parameter.place:
            parameter.place = 59  # Default place ID
        if not parameter.withParam:
            parameter.withParam = "future"
        if not parameter.i18n:
            parameter.i18n = "ru"
        if not parameter.type:
            parameter.type = "sport"