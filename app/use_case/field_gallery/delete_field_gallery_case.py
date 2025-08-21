from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.field_gallery.field_gallery_repository import (
    FieldGalleryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteFieldGalleryCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления изображения из галереи поля.

    Использует:
        - Репозиторий `FieldGalleryRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (FieldGalleryRepository): Репозиторий для работы с галереей.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldGalleryEntity | None): Удаляемая модель изображения галереи.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldGalleryRepository(db)
        self.file_service = FileService(db)
        self.model: FieldGalleryEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False, delete_file: bool = True
    ) -> bool:
        """
        Выполняет операцию удаления изображения из галереи поля.

        Args:
            id (int): Идентификатор изображения галереи для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).
            delete_file (bool): Удалять ли связанный файл (по умолчанию True).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id)

        # Удаление связанного файла (если требуется и файл существует)
        if delete_file and self.model.file_id:
            await self.file_service.delete_file(file_id=self.model.file_id)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор изображения галереи для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("gallery_id_validation_error")
            )

        # Проверка существования изображения галереи
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("field_gallery_not_found")
            )

        self.model = model
