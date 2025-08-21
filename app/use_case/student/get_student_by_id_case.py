from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.student.student_dto import StudentWithRelationsRDTO
from app.adapters.repository.student.student_repository import StudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import StudentEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetStudentByIdCase(BaseUseCase[StudentWithRelationsRDTO]):
    """
    Класс Use Case для получения студента по ID.

    Использует:
        - Репозиторий `StudentRepository` для работы с базой данных.
        - DTO `StudentWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (StudentRepository): Репозиторий для работы со студентами.
        model (StudentEntity | None): Найденная модель студента.

    Методы:
        execute(id: int) -> StudentWithRelationsRDTO:
            Выполняет поиск и возвращает студента по ID.
        validate(id: int):
            Валидирует существование студента с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = StudentRepository(db)
        self.model: StudentEntity | None = None

    async def execute(self, id: int) -> StudentWithRelationsRDTO:
        """
        Выполняет операцию получения студента по ID.

        Args:
            id (int): Идентификатор студента.

        Returns:
            StudentWithRelationsRDTO: Объект студента с отношениями.

        Raises:
            AppExceptionResponse: Если студент не найден.
        """
        await self.validate(id=id)
        return StudentWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование студента с данным ID.

        Args:
            id (int): Идентификатор студента для поиска.

        Raises:
            AppExceptionResponse: Если студент не найден.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
