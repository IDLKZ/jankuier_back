from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import FieldPartyScheduleSettingsWithRelationsRDTO
from app.adapters.dto.pagination_dto import PaginationFieldPartyScheduleSettingsWithRelationsRDTO
from app.adapters.filters.field_party_schedule_settings.field_party_schedule_settings_pagination_filter import FieldPartyScheduleSettingsPaginationFilter
from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import FieldPartyScheduleSettingsRepository
from app.use_case.base_case import BaseUseCase


class PaginateFieldPartyScheduleSettingsCase(BaseUseCase[PaginationFieldPartyScheduleSettingsWithRelationsRDTO]):
    """
    Класс Use Case для получения пагинированного списка настроек расписания площадок.

    Использует:
        - Репозиторий `FieldPartyScheduleSettingsRepository` для работы с базой данных.
        - DTO `PaginationFieldPartyScheduleSettingsWithRelationsRDTO` для возврата пагинированных данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками расписания.

    Методы:
        execute() -> PaginationFieldPartyScheduleSettingsWithRelationsRDTO:
            Выполняет запрос и возвращает пагинированный список настроек расписания.
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

    async def execute(self, filter: FieldPartyScheduleSettingsPaginationFilter) -> PaginationFieldPartyScheduleSettingsWithRelationsRDTO:
        """
        Выполняет операцию получения пагинированного списка настроек расписания площадок.

        Args:
            filter (FieldPartyScheduleSettingsPaginationFilter): Фильтр для поиска, сортировки и пагинации.

        Returns:
            PaginationFieldPartyScheduleSettingsWithRelationsRDTO: Пагинированный список настроек расписания с связями.
        """
        pagination_result = await self.repository.paginate(
            dto=FieldPartyScheduleSettingsWithRelationsRDTO,
            order_by=filter.order_by,
            order_direction=filter.order_direction,
            page=filter.page,
            per_page=filter.per_page,
            options=self.repository.default_relationships(),
            filters=filter.apply(),
            include_deleted_filter=filter.is_show_deleted,
        )
        return pagination_result

    async def validate(self) -> None:
        """
        Валидация перед выполнением (пока не используется).
        """
        pass