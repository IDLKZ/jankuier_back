from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
    FieldPartyScheduleSettingsRDTO,
)
from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import (
    FieldPartyScheduleSettingsRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFieldPartyScheduleSettingsByIdCase(
    BaseUseCase[FieldPartyScheduleSettingsRDTO]
):
    """
    Класс Use Case для получения настройки расписания площадки по ID.

    Использует:
        - Репозиторий `FieldPartyScheduleSettingsRepository` для работы с базой данных.
        - DTO `FieldPartyScheduleSettingsRDTO` для возврата данных.

    Атрибуты:
        repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками расписания.

    Методы:
        execute() -> FieldPartyScheduleSettingsRDTO:
            Выполняет запрос и возвращает настройку расписания по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleSettingsRepository(db)

    async def execute(self, id: int) -> FieldPartyScheduleSettingsRDTO:
        """
        Выполняет операцию получения настройки расписания площадки по ID.

        Args:
            id (int): ID настройки расписания.

        Returns:
            FieldPartyScheduleSettingsRDTO: Объект настройки расписания.

        Raises:
            AppExceptionResponse: Если настройка расписания не найдена.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("field_party_schedule_settings_not_found")
            )

        return FieldPartyScheduleSettingsRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID настройки расписания для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(i18n.gettext("id_validation_error"))
