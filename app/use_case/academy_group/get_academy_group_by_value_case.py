from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyGroupByValueCase(BaseUseCase[AcademyGroupRDTO]):
    """
    Класс Use Case для получения группы академии по уникальному значению.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - DTO `AcademyGroupRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.

    Методы:
        execute() -> AcademyGroupRDTO:
            Выполняет запрос и возвращает группу академии по значению.
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

    async def execute(self, value: str) -> AcademyGroupRDTO:
        """
        Выполняет операцию получения группы академии по уникальному значению.

        Args:
            value (str): Уникальное значение группы академии.

        Returns:
            AcademyGroupRDTO: Объект группы академии.

        Raises:
            AppExceptionResponse: Если группа академии не найдена.
        """
        await self.validate(value)

        model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            include_deleted_filter=True,
        )
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_group_not_found")
            )

        return AcademyGroupRDTO.from_orm(model)

    async def validate(self, value: str) -> None:
        """
        Валидация входных данных.

        Args:
            value (str): Значение группы академии для валидации.

        Raises:
            AppExceptionResponse: Если значение недействительно.
        """
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise AppExceptionResponse.bad_request(
                "Значение группы академии не может быть пустым"
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass
