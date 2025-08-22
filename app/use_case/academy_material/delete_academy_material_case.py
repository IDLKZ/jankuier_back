from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.academy_material.academy_material_repository import (
    AcademyMaterialRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyMaterialEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteAcademyMaterialCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления материала академии.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyMaterialEntity | None): Удаляемая модель материала.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyMaterialRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyMaterialEntity | None = None

    async def execute(
        self, id: int, force_delete: bool = False, delete_file: bool = True
    ) -> bool:
        """
        Выполняет операцию удаления материала академии.

        Args:
            id (int): Идентификатор материала академии для удаления.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).
            delete_file (bool): Удалять ли связанный файл материала (по умолчанию True).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, force_delete=force_delete)

        # Удаление связанного файла материала (если требуется и файл существует)
        if delete_file and self.model.file_id:
            await self.file_service.delete_file(file_id=self.model.file_id)

        result = await self.repository.delete(id, force_delete=force_delete)
        return result

    async def validate(self, id: int, force_delete: bool = False) -> None:
        """
        Валидация перед выполнением удаления.

        Args:
            id (int): Идентификатор материала академии для валидации.
            force_delete (bool): Принудительное удаление.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка валидности ID
        if not isinstance(id, int) or id <= 0:
            raise AppExceptionResponse.bad_request(
                i18n.gettext("academy_material_id_validation_error")
            )

        # Проверка существования материала академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                i18n.gettext("academy_material_not_found")
            )

        # Бизнес-правила для удаления
        if not force_delete:
            # Дополнительные бизнес-проверки (если нужны):
            # - Проверка на использование материала в других местах
            # - Проверка прав доступа к материалу
            # - Другие бизнес-ограничения
            pass

        self.model = model

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass