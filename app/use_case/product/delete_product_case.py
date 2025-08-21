from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteProductCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления товара.

    Использует:
        - Репозиторий `ProductRepository` для работы с базой данных.
        - `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (ProductRepository): Репозиторий для работы с товарами.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductEntity | None): Модель товара для удаления.
        file_id (int | None): ID файла изображения для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление товара.
        validate(id: int):
            Валидирует возможность удаления товара.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductRepository(db)
        self.file_service = FileService(db)
        self.model: ProductEntity | None = None
        self.file_id: int | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления товара.

        Args:
            id (int): Идентификатор товара.
            force_delete (bool): Флаг принудительного удаления (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)
        
        # Удаление связанного файла изображения при успешном удалении товара
        if self.file_id and result:
            await self.file_service.delete_file(file_id=self.file_id)
        
        return result

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления товара.

        Args:
            id (int): Идентификатор товара.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))
        
        # Запоминаем ID файла для удаления
        if self.model.image_id:
            self.file_id = self.model.image_id