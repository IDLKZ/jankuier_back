from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
    RequestToAcademyGroupWithRelationsRDTO,
)
from app.adapters.repository.request_to_academy_group.request_to_academy_group_repository import (
    RequestToAcademyGroupRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import RequestToAcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetRequestToAcademyGroupByIdCase(
    BaseUseCase[RequestToAcademyGroupWithRelationsRDTO]
):
    """
    Класс Use Case для получения заявки в академическую группу по ID.

    Использует:
        - Репозиторий `RequestToAcademyGroupRepository` для работы с базой данных.
        - DTO `RequestToAcademyGroupWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (RequestToAcademyGroupRepository): Репозиторий для работы с заявками в академические группы.
        model (RequestToAcademyGroupEntity | None): Найденная модель заявки в академическую группу.

    Методы:
        execute(id: int) -> RequestToAcademyGroupWithRelationsRDTO:
            Выполняет поиск и возвращает заявку в академическую группу по ID.
        validate(id: int):
            Валидирует существование заявки в академическую группу с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = RequestToAcademyGroupRepository(db)
        self.model: RequestToAcademyGroupEntity | None = None

    async def execute(self, id: int) -> RequestToAcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию получения заявки в академическую группу по ID.

        Args:
            id (int): Идентификатор заявки в академическую группу.

        Returns:
            RequestToAcademyGroupWithRelationsRDTO: Объект заявки в академическую группу с отношениями.

        Raises:
            AppExceptionResponse: Если заявка в академическую группу не найдена.
        """
        await self.validate(id=id)
        return RequestToAcademyGroupWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование заявки в академическую группу с данным ID.

        Args:
            id (int): Идентификатор заявки в академическую группу для поиска.

        Raises:
            AppExceptionResponse: Если заявка в академическую группу не найдена.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
