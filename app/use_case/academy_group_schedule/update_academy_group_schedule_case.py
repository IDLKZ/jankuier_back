from datetime import datetime, date, time
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import AcademyGroupScheduleUpdateDTO, AcademyGroupScheduleWithRelationsRDTO
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import AcademyGroupScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateAcademyGroupScheduleCase(BaseUseCase[AcademyGroupScheduleWithRelationsRDTO]):
    """
    Класс Use Case для обновления расписания группы академии.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.
        - DTO `AcademyGroupScheduleUpdateDTO` для входных данных.
        - DTO `AcademyGroupScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.
        model (AcademyGroupScheduleEntity | None): Обновляемая модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupScheduleRepository(db)
        self.model: AcademyGroupScheduleEntity | None = None

    async def execute(
        self, id: int, dto: AcademyGroupScheduleUpdateDTO
    ) -> AcademyGroupScheduleWithRelationsRDTO:
        """
        Выполняет операцию обновления расписания группы академии.

        Args:
            id (int): Идентификатор расписания.
            dto (AcademyGroupScheduleUpdateDTO): Данные для обновления расписания.

        Returns:
            AcademyGroupScheduleWithRelationsRDTO: Обновленное расписание с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupScheduleWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int, dto: AcademyGroupScheduleUpdateDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор расписания.
            dto (AcademyGroupScheduleUpdateDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("academy_group_schedule_not_found")
            )

        # Проверка: нельзя изменять завершенную тренировку
        if model.is_finished:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_cannot_update_finished")
            )

        # Проверка: если тренировка уже началась, ограничения на изменения
        current_datetime = datetime.now()
        training_datetime = datetime.combine(model.training_date, model.start_at)
        
        if current_datetime >= training_datetime:
            # Если тренировка началась, можно изменить только статусы
            allowed_fields = ['is_canceled', 'is_finished', 'reschedule_start_at', 'reschedule_end_at']
            for field, value in dto.dict(exclude_unset=True).items():
                if field not in allowed_fields and value is not None:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("schedule_already_started")
                    )

        # Валидация времени: время начала должно быть раньше времени окончания
        start_at = dto.start_at if dto.start_at is not None else model.start_at
        end_at = dto.end_at if dto.end_at is not None else model.end_at
        
        if start_at >= end_at:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_time_validation_error")
            )

        # Валидация даты: дата тренировки не может быть в прошлом (только при изменении даты)
        if dto.training_date is not None and dto.training_date < date.today():
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_date_validation_error")
            )

        # Валидация времени переноса (если обновляется)
        reschedule_start = dto.reschedule_start_at if dto.reschedule_start_at is not None else model.reschedule_start_at
        reschedule_end = dto.reschedule_end_at if dto.reschedule_end_at is not None else model.reschedule_end_at

        if reschedule_start and reschedule_end:
            if reschedule_start >= reschedule_end:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("reschedule_time_validation_error")
                )

        # Проверка статусов: нельзя отменить завершенную тренировку
        if dto.is_canceled is True and model.is_finished:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_cannot_cancel_finished")
            )

        # Проверка на конфликты с существующими расписаниями (только если изменяется время или дата)
        if any([dto.training_date, dto.start_at, dto.end_at]):
            training_date = dto.training_date if dto.training_date is not None else model.training_date
            
            existing_schedules = await self.repository.get_with_filters(
                filters=[
                    self.repository.model.group_id == model.group_id,
                    self.repository.model.training_date == training_date,
                    self.repository.model.is_active == True,
                    self.repository.model.is_canceled == False,
                    self.repository.model.id != id,  # Исключаем текущее расписание
                    and_(
                        # Проверка пересечения времени
                        start_at < self.repository.model.end_at,
                        end_at > self.repository.model.start_at
                    )
                ]
            )
            
            if existing_schedules:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("schedule_conflict_error")
                )

    async def transform(self, id: int, dto: AcademyGroupScheduleUpdateDTO) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор расписания.
            dto (AcademyGroupScheduleUpdateDTO): Данные для преобразования.
        """
        self.model = await self.repository.get(id)