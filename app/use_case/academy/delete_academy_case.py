from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteAcademyCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления академии.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyEntity | None): Удаляемая модель академии.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False, delete_image: bool = True
    ) -> bool:
        """
        Выполняет операцию удаления академии.

        Args:
            id (int): Идентификатор академии для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).
            delete_image (bool): Удалять ли связанное изображение (по умолчанию True).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)

        # Удаление связанного изображения (если требуется и изображение существует)
        if delete_image and self.model.image_id:
            await self.file_service.delete_file(file_id=self.model.image_id)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор академии для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_id_validation_error")
            )

        # Проверка существования академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(i18n.gettext("academy_not_found"))

        # Бизнес-правила для удаления
        if not force_delete:
            # Здесь можно добавить дополнительные проверки:
            # - Проверка на существование связанных групп
            # - Проверка на активных студентов
            # - Другие бизнес-ограничения
            pass

        self.model = model
