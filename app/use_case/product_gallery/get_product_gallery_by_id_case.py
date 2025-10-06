from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product_gallery.product_gallery_dto import (
    ProductGalleryWithRelationsRDTO,
)
from app.adapters.repository.product_gallery.product_gallery_repository import (
    ProductGalleryRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductGalleryEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetProductGalleryByIdCase(BaseUseCase[ProductGalleryWithRelationsRDTO]):
    """
    Класс Use Case для получения изображения галереи товара по ID.

    Использует:
        - Репозиторий `ProductGalleryRepository` для работы с базой данных.
        - DTO `ProductGalleryWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ProductGalleryRepository): Репозиторий для работы с изображениями галереи товаров.
        model (ProductGalleryEntity | None): Найденная модель изображения галереи товара.

    Методы:
        execute(id: int) -> ProductGalleryWithRelationsRDTO:
            Выполняет поиск и возвращает изображение галереи товара по ID.
        validate(id: int):
            Валидирует существование изображения галереи товара с данным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ProductGalleryRepository(db)
        self.model: ProductGalleryEntity | None = None

    async def execute(self, id: int) -> ProductGalleryWithRelationsRDTO:
        """
        Выполняет операцию получения изображения галереи товара по ID.

        Args:
            id (int): Идентификатор изображения галереи товара.

        Returns:
            ProductGalleryWithRelationsRDTO: Объект изображения галереи товара с отношениями.

        Raises:
            AppExceptionResponse: Если изображение галереи товара не найдено.
        """
        await self.validate(id=id)
        return ProductGalleryWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование изображения галереи товара с данным ID.

        Args:
            id (int): Идентификатор изображения галереи товара для поиска.

        Raises:
            AppExceptionResponse: Если изображение галереи товара не найдено.
        """
        self.model = await self.repository.get(
            id=id,
            options=self.repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.model:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
