from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductVariantEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.use_case.base_case import BaseUseCase


class DeleteProductVariantCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления варианта товара.

    Использует:
        - Репозиторий `ProductVariantRepository` для работы с базой данных.
        - `FileService` для удаления связанных файлов.

    Атрибуты:
        repository (ProductVariantRepository): Репозиторий для работы с вариантами товаров.
        file_service (FileService): Сервис для работы с файлами.
        model (ProductVariantEntity | None): Модель варианта товара для удаления.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Выполняет удаление варианта товара.
        validate(id: int):
            Валидирует возможность удаления варианта товара.
        transform(force_delete: bool = False):
            Трансформирует операцию удаления.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductVariantRepository(db)
        self.file_service = FileService(db)
        self.model: ProductVariantEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления варианта товара.

        Args:
            id (int): Идентификатор варианта товара для удаления.
            force_delete (bool): Флаг принудительного удаления (полное удаление из БД).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если вариант товара не найден или удаление невозможно.
        """
        await self.validate(id=id)
        await self.transform(force_delete=force_delete)
        return True

    async def validate(self, id: int) -> None:
        """
        Валидирует возможность удаления варианта товара.

        Args:
            id (int): Идентификатор варианта товара для удаления.

        Raises:
            AppExceptionResponse: Если вариант товара не найден.
        """
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, force_delete: bool = False):
        """
        Трансформирует операцию удаления варианта товара.

        Args:
            force_delete (bool): Флаг принудительного удаления.
        """
        # Удаление связанного файла изображения при полном удалении
        if force_delete and self.model.image_id:
            await self.file_service.delete_file(file_id=self.model.image_id)

        # Выполнение удаления
        await self.repository.delete(id=self.model.id, force_delete=force_delete)