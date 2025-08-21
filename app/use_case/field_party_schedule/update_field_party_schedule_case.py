from decimal import Decimal
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party_schedule.field_party_schedule_dto import (
    FieldPartyScheduleUpdateDTO,
    FieldPartyScheduleWithRelationsRDTO,
)
from app.adapters.repository.field_party_schedule.field_party_schedule_repository import (
    FieldPartyScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateFieldPartyScheduleCase(BaseUseCase[FieldPartyScheduleWithRelationsRDTO]):
    """
    Класс Use Case для обновления расписания площадки.

    Использует:
        - Репозиторий `FieldPartyScheduleRepository` для работы с базой данных.
        - DTO `FieldPartyScheduleUpdateDTO` для входных данных.
        - DTO `FieldPartyScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyScheduleRepository): Репозиторий для работы с расписаниями.
        model (FieldPartyScheduleEntity | None): Обновляемая модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyScheduleRepository(db)
        self.model: FieldPartyScheduleEntity | None = None

    async def execute(
        self, id: int, dto: FieldPartyScheduleUpdateDTO
    ) -> FieldPartyScheduleWithRelationsRDTO:
        """
        Выполняет операцию обновления расписания площадки.

        Args:
            id (int): Идентификатор расписания площадки.
            dto (FieldPartyScheduleUpdateDTO): Данные для обновления расписания площадки.

        Returns:
            FieldPartyScheduleWithRelationsRDTO: Обновленное расписание площадки с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldPartyScheduleWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: FieldPartyScheduleUpdateDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор расписания площадки.
            dto (FieldPartyScheduleUpdateDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("field_party_schedule_not_found")
            )

        # Проверка, что расписание не забронировано (если пытаемся изменить время или дату)
        if (
            dto.day is not None or dto.start_at is not None or dto.end_at is not None
        ) and model.is_booked:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_already_booked_error")
            )

        # Проверка, что расписание не оплачено (если пытаемся изменить критичные параметры)
        if (
            dto.day is not None
            or dto.start_at is not None
            or dto.end_at is not None
            or dto.price is not None
        ) and model.is_paid:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_already_paid_error")
            )

        # Валидация времени начала и окончания
        start_time = dto.start_at if dto.start_at is not None else model.start_at
        end_time = dto.end_at if dto.end_at is not None else model.end_at

        if start_time >= end_time:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("time_period_validation_error")
            )

        # Валидация цены
        if dto.price is not None and dto.price <= Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("price_validation_error")
            )

        # Проверка на пересечение времени с существующими расписаниями (если изменяем время или дату)
        if dto.day is not None or dto.start_at is not None or dto.end_at is not None:
            await self._check_time_overlap(id, model, dto)

    async def _check_time_overlap(
        self, id: int, model: FieldPartyScheduleEntity, dto: FieldPartyScheduleUpdateDTO
    ) -> None:
        """
        Проверка на пересечение времени с существующими расписаниями.

        Args:
            id (int): ID текущего расписания (исключаем из проверки).
            model (FieldPartyScheduleEntity): Текущая модель расписания.
            dto (FieldPartyScheduleUpdateDTO): Данные для обновления.

        Raises:
            AppExceptionResponse: Если найдено пересечение.
        """
        # Определяем финальные значения после обновления
        party_id = model.party_id
        day = dto.day if dto.day is not None else model.day
        start_at = dto.start_at if dto.start_at is not None else model.start_at
        end_at = dto.end_at if dto.end_at is not None else model.end_at

        # Проверяем пересечение времени в тот же день на той же площадке
        existing_schedules = await self.repository.get_with_filters(
            filters=[
                and_(
                    FieldPartyScheduleEntity.id != id,  # Исключаем текущее расписание
                    FieldPartyScheduleEntity.party_id == party_id,
                    FieldPartyScheduleEntity.day == day,
                    # Проверяем пересечение времени
                    and_(
                        start_at < FieldPartyScheduleEntity.end_at,
                        end_at > FieldPartyScheduleEntity.start_at,
                    ),
                )
            ]
        )

        if existing_schedules:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_overlap_error")
            )

    async def transform(self, id: int, dto: FieldPartyScheduleUpdateDTO) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор расписания площадки.
            dto (FieldPartyScheduleUpdateDTO): Данные для преобразования.
        """
        self.model = await self.repository.get(id)
