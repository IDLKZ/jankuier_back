from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group_schedule.academy_group_schedule_dto import (
    AcademyGroupScheduleRDTO,
)
from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import (
    AcademyGroupScheduleRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyGroupScheduleByIdCase(BaseUseCase[AcademyGroupScheduleRDTO]):
    """
    Класс Use Case для получения расписания группы академии по ID.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.
        - DTO `AcademyGroupScheduleRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.

    Методы:
        execute() -> AcademyGroupScheduleRDTO:
            Выполняет запрос и возвращает расписание по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupScheduleRepository(db)

    async def execute(self, id: int) -> AcademyGroupScheduleRDTO:
        """
        Выполняет операцию получения расписания группы академии по ID.

        Args:
            id (int): ID расписания.

        Returns:
            AcademyGroupScheduleRDTO: Объект расписания.

        Raises:
            AppExceptionResponse: Если расписание не найдено.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_group_schedule_not_found")
            )

        return AcademyGroupScheduleRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID расписания для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_group_schedule_id_validation_error")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
