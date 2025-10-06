from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import (
    FieldPartyScheduleSettingsRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyScheduleSettingsEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteFieldPartyScheduleSettingsCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления настроек расписания площадки.

    Использует:
        - Репозиторий `FieldPartyScheduleSettingsRepository` для работы с базой данных.

    Атрибуты:
        repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками расписания.
        model (FieldPartyScheduleSettingsEntity | None): Удаляемая модель настроек расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleSettingsRepository(db)
        self.model: FieldPartyScheduleSettingsEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления настроек расписания площадки.

        Args:
            id (int): Идентификатор настроек расписания для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор настроек расписания для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(i18n.gettext("id_validation_error"))

        # Проверка существования настроек расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("field_party_schedule_settings_not_found")
            )

        self.model = model
