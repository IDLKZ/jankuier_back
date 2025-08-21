from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyRDTO
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyByIdCase(BaseUseCase[AcademyRDTO]):
    """
    Класс Use Case для получения академии по ID.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - DTO `AcademyRDTO` для возврата данных.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.

    Методы:
        execute() -> AcademyRDTO:
            Выполняет запрос и возвращает академию по ID.
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

    async def execute(self, id: int) -> AcademyRDTO:
        """
        Выполняет операцию получения академии по ID.

        Args:
            id (int): ID академии.

        Returns:
            AcademyRDTO: Объект академии.

        Raises:
            AppExceptionResponse: Если академия не найдена.
        """
        await self.validate(id)
        
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_not_found")
            )
        
        return AcademyRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных данных.

        Args:
            id (int): ID академии для валидации.

        Raises:
            AppExceptionResponse: Если ID недействителен.
        """
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_id_validation_error")
            )