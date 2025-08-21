from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.student.student_repository import StudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import StudentEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteStudentCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления студента.

    Использует:
        - Репозиторий `StudentRepository` для работы с базой данных.
        - `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (StudentRepository): Репозиторий для работы со студентами.
        file_service (FileService): Сервис для работы с файлами.
        model (StudentEntity | None): Модель студента для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление студента.
        validate(id: int):
            Валидирует возможность удаления студента.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = StudentRepository(db)
        self.file_service = FileService(db)
        self.model: StudentEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления студента.

        Args:
            id (int): Идентификатор студента для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если студент не найден или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления студента.

        Args:
            id (int): Идентификатор студента для удаления.

        Raises:
            AppExceptionResponse: Если студент не найден.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления студента.

        Args:
            force_delete (bool): Флаг принудительного удаления.
        """
        # Удаление связанного файла фотографии при полном удалении
        if force_delete and self.model.image_id:
            await self.file_service.delete_file(file_id=self.model.image_id)

        # Выполнение удаления
        await self.repository.delete(id=self.model.id, force_delete=force_delete)