from datetime import time
from decimal import Decimal
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleCDTO,
    FieldPartyScheduleWithRelationsRDTO,
)
from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.adapters.repository.field_party_schedule_settings.field_party_schedule_settings_repository import (
    FieldPartyScheduleSettingsRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateFieldPartyScheduleCase(BaseUseCase[FieldPartyScheduleWithRelationsRDTO]):
    """
    Класс Use Case для создания нового расписания площадки.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.
        - Репозиторий `FieldPartyRepository` для проверки существования площадки.
        - Репозиторий `FieldPartyScheduleSettingsRepository` для проверки существования настроек.
        - DTO `FieldPartyScheduleCDTO` для входных данных.
        - DTO `FieldPartyScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями.
        field_party_repository (FieldPartyRepository): Репозиторий для работы с площадками.
        settings_repository (FieldPartyScheduleSettingsRepository): Репозиторий для работы с настройками.
        model (FieldPartyScheduleEntity | None): Созданная модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleRepository(db)
        self.field_party_repository = FieldPartyRepository(db)
        self.settings_repository = FieldPartyScheduleSettingsRepository(db)
        self.model: FieldPartyScheduleEntity | None = None

    async def execute(
        self, dto: FieldPartyScheduleCDTO
    ) -> FieldPartyScheduleWithRelationsRDTO:
        """
        Выполняет операцию создания расписания площадки.

        Args:
            dto (FieldPartyScheduleCDTO): Данные для создания расписания площадки.

        Returns:
            FieldPartyScheduleWithRelationsRDTO: Созданное расписание площадки с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldPartyScheduleWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: FieldPartyScheduleCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (FieldPartyScheduleCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования площадки
        field_party = await self.field_party_repository.get(dto.party_id)
        if not field_party:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("field_party_not_found")
            )

        # Проверка существования настроек расписания
        settings = await self.settings_repository.get(dto.setting_id)
        if not settings:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("field_party_schedule_settings_not_found")
            )

        # Валидация времени начала и окончания
        if dto.start_at >= dto.end_at:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("time_period_validation_error")
            )

        # Валидация цены
        if dto.price <= Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("price_validation_error")
            )

        # Проверка на пересечение времени с существующими расписаниями
        await self._check_time_overlap(dto)

    async def _check_time_overlap(self, dto: FieldPartyScheduleCDTO) -> None:
        """
        Проверка на пересечение времени с существующими расписаниями.

        Args:
            dto (FieldPartyScheduleCDTO): Данные для проверки.

        Raises:
            AppExceptionResponse: Если найдено пересечение.
        """
        # Проверяем пересечение времени в тот же день на той же площадке
        existing_schedules = await self.repository.get_with_filters(
            filters=[
                and_(
                    FieldPartyScheduleEntity.party_id == dto.party_id,
                    FieldPartyScheduleEntity.day == dto.day,
                    # Проверяем пересечение времени:
                    # Новое расписание пересекается если:
                    # (start_at < existing_end_at) AND (end_at > existing_start_at)
                    and_(
                        dto.start_at < FieldPartyScheduleEntity.end_at,
                        dto.end_at > FieldPartyScheduleEntity.start_at,
                    ),
                )
            ]
        )

        if existing_schedules:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_overlap_error")
            )

    async def transform(self, dto: FieldPartyScheduleCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (FieldPartyScheduleCDTO): Данные для преобразования.
        """
        self.model = FieldPartyScheduleEntity(**dto.dict())
