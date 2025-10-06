from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyRDTO
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyByValueCase(BaseUseCase[AcademyRDTO]):
    """
    Класс Use Case для получения академии по уникальному значению.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - DTO `AcademyRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.

    Методы:
        execute() -> AcademyRDTO:
            Выполняет запрос и возвращает академию по значению.
        validate():
            Валидация входных данных.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyRepository(db)

    async def execute(self, value: str) -> AcademyRDTO:
        """
        Выполняет операцию получения академии по уникальному значению.

        Args:
            value (str): Уникальное значение академии.

        Returns:
            AcademyRDTO: Объект академии.

        Raises:
            AppExceptionResponse: Если академия не найдена.
        """
        await self.validate(value)

        model = await self.repository.get_first_with_filters(
            filters=[func.lower(self.repository.model.value) == value.lower()],
            include_deleted_filter=True,
        )
        if not model:
            raise AppExceptionResponse.bad_request(i18n.gettext("academy_not_found"))

        return AcademyRDTO.from_orm(model)

    async def validate(self, value: str) -> None:
        """
        Валидация входных данных.

        Args:
            value (str): Значение академии для валидации.

        Raises:
            AppExceptionResponse: Если значение недействительно.
        """
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise AppExceptionResponse.bad_request(
                "Значение академии не может быть пустым"
            )
