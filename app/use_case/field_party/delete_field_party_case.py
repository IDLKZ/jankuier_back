from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteFieldPartyByIdCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления площадки поля по ID.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldPartyEntity | None): Удаляемая модель площадки поля.
        file_id (int | None): ID связанного файла для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет площадку поля и возвращает результат операции.
        validate(id: int):
            Проверяет существование площадки поля.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)
        self.file_service = FileService(db)
        self.model: FieldPartyEntity | None = None
        self.file_id: int | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления площадки поля.

        Args:
            id (int): Идентификатор площадки поля.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)

        # Удаление связанного файла при успешном удалении
        if self.file_id and result:
            await self.file_service.delete_file(file_id=self.file_id)

        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор площадки поля для проверки.

        Raises:
            AppExceptionResponse: Если площадка поля не найдена.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))

        # Сохранение ID файла для последующего удаления
        if self.model.image_id:
            self.file_id = self.model.image_id
