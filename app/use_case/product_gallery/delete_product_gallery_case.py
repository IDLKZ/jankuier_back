from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_gallery.product_gallery_repository import (
    ProductGalleryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteProductGalleryCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления изображения из галереи товара.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductGalleryEntity | None): Модель изображения галереи товара для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление изображения из галереи товара.
        validate(id: int):
            Валидирует возможность удаления изображения галереи товара.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductGalleryRepository(db)
        self.file_service = FileService(db)
        self.model: ProductGalleryEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления изображения из галереи товара.

        Args:
            id (int): Идентификатор изображения галереи товара для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).
                                 Примечание: ProductGallery не поддерживает soft delete (нет поля deleted_at).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если изображение галереи товара не найдено или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления изображения галереи товара.

        Args:
            id (int): Идентификатор изображения галереи товара для удаления.

        Raises:
            AppExceptionResponse: Если изображение галереи товара не найдено.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления изображения галереи товара.

        Args:
            force_delete (bool): Флаг принудительного удаления.
                                Примечание: ProductGallery всегда удаляется полностью (нет поля deleted_at).
        """
        # Удаление связанного файла при полном удалении (если файл существует)
        if self.model.file_id:
            await self.file_service.delete_file(file_id=self.model.file_id)

        # Выполнение удаления (всегда force_delete=True, так как нет поля deleted_at)
        await self.repository.delete(id=self.model.id, force_delete=True)
