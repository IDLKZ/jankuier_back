from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import (
    FieldPartyScheduleSettingsWithRelationsRDTO,
)
from app.adapters.filters.field_party_schedule_settings.field_party_schedule_settings_filter import (
    FieldPartyScheduleSettingsFilter,
)
from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import (
    FieldPartyScheduleSettingsRepository,
)
from app.use_case.base_case import BaseUseCase


class AllFieldPartyScheduleSettingsCase(
    BaseUseCase[list[FieldPartyScheduleSettingsWithRelationsRDTO]]
):
    """
    Класс Use Case для получения списка всех настроек расписания площадок.

    Использует:
        - Репозиторий `FieldPartyScheduleSettingsRepository` для работы с базой данных.
        - DTO `FieldPartyScheduleSettingsWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками расписания.

    Методы:
        execute() -> list[FieldPartyScheduleSettingsWithRelationsRDTO]:
            Выполняет запрос и возвращает список всех настроек расписания.
        validate():
            Метод валидации (пока пустой, но можно использовать для проверок).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleSettingsRepository(db)

    async def execute(
        self, filter: FieldPartyScheduleSettingsFilter
    ) -> list[FieldPartyScheduleSettingsWithRelationsRDTO]:
        """
        Выполняет операцию получения списка всех настроек расписания площадок.

        Args:
            filter (FieldPartyScheduleSettingsFilter): Фильтр для поиска и сортировки.

        Returns:
            list[FieldPartyScheduleSettingsWithRelationsRDTO]: Список объектов настроек расписания с связями.
        """
        models = await self.repository.get_with_filters(
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return [
            FieldPartyScheduleSettingsWithRelationsRDTO.from_orm(model)
            for model in models
        ]

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass
