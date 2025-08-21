from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.academy_group_schedule.academy_group_schedule_repository import AcademyGroupScheduleRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupScheduleEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteAcademyGroupScheduleCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления расписания группы академии.

    Использует:
        - Репозиторий `AcademyGroupScheduleRepository` для работы с базой данных.

    Атрибуты:
        repository (AcademyGroupScheduleRepository): Репозиторий для работы с расписаниями.
        model (AcademyGroupScheduleEntity | None): Удаляемая модель расписания.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupScheduleRepository(db)
        self.model: AcademyGroupScheduleEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления расписания группы академии.

        Args:
            id (int): Идентификатор расписания для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)
        
        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор расписания для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_group_schedule_id_validation_error")
            )

        # Проверка существования расписания
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_group_schedule_not_found")
            )

        # Бизнес-правила для удаления
        if not force_delete:
            # Проверка: нельзя удалять завершенную тренировку
            if model.is_finished:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("schedule_cannot_update_finished")
                )
            
            # Проверка: нельзя удалять расписание, если тренировка уже началась
            current_datetime = datetime.now()
            training_datetime = datetime.combine(model.training_date, model.start_at)
            
            if current_datetime >= training_datetime and not model.is_canceled:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("schedule_already_started")
                )

            # Дополнительные бизнес-проверки (если нужны):
            # - Проверка на существование связанных записей посещаемости
            # - Проверка на платежи за данную тренировку
            # - Другие связанные записи
            pass

        self.model = model

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass