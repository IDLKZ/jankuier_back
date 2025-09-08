from app.adapters.dto.ticketon.ticketon_single_show_dto import TicketonSingleShowResponseDTO
from app.core.app_exception_response import AppExceptionResponse
from app.infrastructure.service.ticketon_service.ticketon_service_api import TicketonServiceAPI
from app.use_case.base_case import BaseUseCase
from app.i18n.i18n_wrapper import i18n


class GetTicketonSingleShowCase(BaseUseCase[TicketonSingleShowResponseDTO]):
    """
    Use Case для получения подробной информации о сеансе Ticketon.
    Получает детальные данные о конкретном сеансе через TicketonServiceAPI.
    """

    def __init__(self):
        """
        Инициализация use case для работы с данными одного сеанса Ticketon.
        """
        self.ticketon_service = TicketonServiceAPI()

    async def execute(self, show_id: int) -> TicketonSingleShowResponseDTO:
        """
        Основная логика получения данных о конкретном сеансе Ticketon.
        
        Args:
            show_id: ID сеанса для получения детальной информации
            
        Returns:
            TicketonSingleShowResponseDTO: Подробные данные о сеансе включая:
                - информацию о сеансе
                - данные события
                - информацию о месте проведения
                - данные зала и схему мест
                - цены на билеты
        """
        await self.validate(show_id)
        await self.transform(show_id)
        
        try:
            return await self.ticketon_service.get_ticketon_single_show(show_id)
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("ticketon_single_show_fetch_error"),
                extra={"details": str(e), "show_id": show_id},
                is_custom=True,
            ) from e

    async def validate(self, show_id: int):
        """
        Валидация ID сеанса для запроса к Ticketon API.
        
        Args:
            show_id: ID сеанса для валидации
            
        Raises:
            AppExceptionResponse: При некорректном ID сеанса
        """
        if not show_id:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_show_id_required"),
                is_custom=True,
            )
            
        if not isinstance(show_id, int) or show_id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("ticketon_invalid_show_id"),
                extra={"show_id": show_id},
                is_custom=True,
            )

    async def transform(self, show_id: int):
        """
        Трансформация ID сеанса перед запросом.
        При необходимости можно добавить логику предобработки ID.
        
        Args:
            show_id: ID сеанса для трансформации
        """
        # Дополнительная логика трансформации может быть добавлена здесь
        # Например, логирование запроса или дополнительная валидация
        pass