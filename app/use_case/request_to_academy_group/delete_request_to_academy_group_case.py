from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import (
    RequestToAcademyGroupRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestToAcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteRequestToAcademyGroupCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления заявки в академическую группу.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.
        model (RequestToAcademyGroupEntity | None): Модель заявки в академическую группу для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление заявки в академическую группу.
        validate(id: int):
            Валидирует возможность удаления заявки в академическую группу.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RequestToAcademyGroupRepository(db)
        self.model: RequestToAcademyGroupEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления заявки в академическую группу.

        Args:
            id (int): Идентификатор заявки в академическую группу для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если заявка в академическую группу не найдена или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления заявки в академическую группу.

        Args:
            id (int): Идентификатор заявки в академическую группу для удаления.

        Raises:
            AppExceptionResponse: Если заявка в академическую группу не найдена или удаление запрещено.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Бизнес-правило: нельзя удалить принятую заявку без принудительного удаления
        if self.model.status == 1 and not force_delete:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("cannot_delete_accepted_request")
            )

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления заявки в академическую группу.

        Args:
            force_delete (bool): Флаг принудительного удаления.
        """
        # Выполнение удаления
        await self.repository.delete(id=self.model.id, force_delete=force_delete)
