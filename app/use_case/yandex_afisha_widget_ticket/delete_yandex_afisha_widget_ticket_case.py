from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.yandex_afisha_widget_ticket.yandex_afisha_widget_ticket_repository import (
    YandexAfishaWidgetTicketRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import YandexAfishaWidgetTicketEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteYandexAfishaWidgetTicketCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления билета Яндекс.Афиша по ID.

    Использует:
        - Репозиторий `YandexAfishaWidgetTicketRepository` для работы с базой данных.
        - Сервис `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (YandexAfishaWidgetTicketRepository): Репозиторий для работы с билетами.
        file_service (FileService): Сервис для работы с файлами.
        model (YandexAfishaWidgetTicketEntity | None): Удаляемая модель билета.
        file_id (int | None): ID связанного файла для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет билет и возвращает результат операции.
        validate(id: int):
            Проверяет существование билета.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = YandexAfishaWidgetTicketRepository(db)
        self.file_service = FileService(db)
        self.model: YandexAfishaWidgetTicketEntity | None = None
        self.file_id: int | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления билета Яндекс.Афиша.

        Args:
            id (int): Идентификатор билета.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если билет не найден.
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
            id (int): Идентификатор билета для проверки.

        Raises:
            AppExceptionResponse: Если билет не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("yandex_afisha_widget_ticket_not_found")
            )

        # Сохранение ID файла для последующего удаления
        if self.model.image_id:
            self.file_id = self.model.image_id
