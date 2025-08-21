from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_category.product_category_repository import (
    ProductCategoryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductCategoryEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteProductCategoryCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления категории товаров.

    Использует:
        - Репозиторий `ProductCategoryRepository` для работы с базой данных.
        - `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (ProductCategoryRepository): Репозиторий для работы с категориями товаров.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductCategoryEntity | None): Модель категории товара для удаления.
        file_id (int | None): ID файла изображения для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление категории товара.
        validate(id: int):
            Валидирует возможность удаления категории товара.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductCategoryRepository(db)
        self.file_service = FileService(db)
        self.model: ProductCategoryEntity | None = None
        self.file_id: int | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления категории товара.

        Args:
            id (int): Идентификатор категории товара.
            force_delete (bool): Флаг принудительного удаления (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)

        # Удаление связанного файла изображения при успешном удалении категории
        if self.file_id and result:
            await self.file_service.delete_file(file_id=self.file_id)

        return result

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления категории товара.

        Args:
            id (int): Идентификатор категории товара.

        Raises:
            AppExceptionResponse: Если категория товара не найдена.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Запоминаем ID файла для удаления
        if self.model.image_id:
            self.file_id = self.model.image_id
