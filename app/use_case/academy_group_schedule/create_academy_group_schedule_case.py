from datetime import datetime, date, time
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import AcademyGroupScheduleCDTO, AcademyGroupScheduleWithRelationsRDTO
from app.adapters.repository.academy_group.academy_group_repository import AcademyGroupRepository
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import AcademyGroupScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateAcademyGroupScheduleCase(BaseUseCase[AcademyGroupScheduleWithRelationsRDTO]):
    """
    Класс Use Case для создания нового расписания группы академии.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.
        - Репозиторий `AcademyGroupRepository` для проверки существования группы.
        - DTO `AcademyGroupScheduleCDTO` для входных данных.
        - DTO `AcademyGroupScheduleWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.
        group_repository (AcademyGroupRepository): Репозиторий для работы с группами.
        model (AcademyGroupScheduleEntity | None): Созданная модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupScheduleRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.model: AcademyGroupScheduleEntity | None = None

    async def execute(self, dto: AcademyGroupScheduleCDTO) -> AcademyGroupScheduleWithRelationsRDTO:
        """
        Выполняет операцию создания расписания группы академии.

        Args:
            dto (AcademyGroupScheduleCDTO): Данные для создания расписания.

        Returns:
            AcademyGroupScheduleWithRelationsRDTO: Созданное расписание с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupScheduleWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: AcademyGroupScheduleCDTO) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (AcademyGroupScheduleCDTO): Данные для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования группы академии
        group = await self.group_repository.get(dto.group_id)
        if not group:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_not_found")
            )

        # Валидация времени: время начала должно быть раньше времени окончания
        if dto.start_at >= dto.end_at:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_time_validation_error")
            )

        # Валидация даты: дата тренировки не может быть в прошлом
        if dto.training_date < date.today():
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_date_validation_error")
            )

        # Валидация времени переноса (если указано)
        if dto.reschedule_start_at and dto.reschedule_end_at:
            if dto.reschedule_start_at >= dto.reschedule_end_at:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("reschedule_time_validation_error")
                )

        # Проверка на конфликты с существующими расписаниями той же группы
        existing_schedules = await self.repository.get_with_filters(
            filters=[
                self.repository.model.group_id == dto.group_id,
                self.repository.model.training_date == dto.training_date,
                self.repository.model.is_active == True,
                self.repository.model.is_canceled == False,
                and_(
                    # Проверка пересечения времени: (start_at < existing_end_at) AND (end_at > existing_start_at)
                    dto.start_at < self.repository.model.end_at,
                    dto.end_at > self.repository.model.start_at
                )
            ]
        )
        
        if existing_schedules:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("schedule_conflict_error")
            )

    async def transform(self, dto: AcademyGroupScheduleCDTO) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (AcademyGroupScheduleCDTO): Данные для преобразования.
        """
        self.model = AcademyGroupScheduleEntity(**dto.dict())