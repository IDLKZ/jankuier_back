from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyGroupByIdCase(BaseUseCase[AcademyGroupRDTO]):
    """
    Класс Use Case для получения группы академии по ID.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - DTO `AcademyGroupRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.

    Методы:
        execute() -> AcademyGroupRDTO:
            Выполняет запрос и возвращает группу академии по ID.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupRepository(db)

    async def execute(self, id: int) -> AcademyGroupRDTO:
        """
        Выполняет операцию получения группы академии по ID.

        Args:
            id (int): ID группы академии.

        Returns:
            AcademyGroupRDTO: Объект группы академии.

        Raises:
            AppExceptionResponse: Если группа академии не найдена.
        """
        await self.validate(id)

        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_group_not_found")
            )

        return AcademyGroupRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID группы академии для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_group_id_validation_error")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
