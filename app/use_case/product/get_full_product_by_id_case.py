from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.product.product_dto import ProductWithRelationsRDTO
from app.adapters.dto.product.full_product_dto import FullProductRDTO
from app.adapters.dto.product_gallery.product_gallery_dto import ProductGalleryWithRelationsRDTO
from app.adapters.dto.product_variant.product_variant_dto import ProductVariantWithRelationsRDTO
from app.adapters.dto.modification_value.modification_value_dto import ModificationValueWithRelationsRDTO
from app.adapters.repository.product.product_repository import ProductRepository
from app.adapters.repository.product_gallery.product_gallery_repository import ProductGalleryRepository
from app.adapters.repository.product_variant.product_variant_repository import ProductVariantRepository
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ProductEntity, ProductGalleryEntity, ProductVariantEntity, ModificationValueEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFullProductByIdCase(BaseUseCase[FullProductRDTO]):
    """
    Класс Use Case для получения полной информации о товаре по ID.
    
    Получает товар со всеми связанными данными:
    - Основная информация о товаре с отношениями
    - Галерея изображений товара
    - Варианты товара
    - Значения модификаций

    Использует:
        - Репозиторий `ProductRepository` для работы с товарами.
        - Репозиторий `ProductGalleryRepository` для работы с галереей.
        - Репозиторий `ProductVariantRepository` для работы с вариантами.
        - Репозиторий `ModificationValueRepository` для работы с модификациями.
        - DTO `FullProductRDTO` для возврата полных данных.

    Атрибуты:
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        gallery_repository (ProductGalleryRepository): Репозиторий для работы с галереей.
        variant_repository (ProductVariantRepository): Репозиторий для работы с вариантами.
        modification_repository (ModificationValueRepository): Репозиторий для работы с модификациями.
        product_model (ProductEntity | None): Найденная модель товара.

    Методы:
        execute(id: int) -> FullProductRDTO:
            Выполняет поиск и возвращает полную информацию о товаре по ID.
        validate(id: int):
            Валидирует существование товара с данным ID.
        transform(id: int) -> FullProductRDTO:
            Преобразует данные в FullProductRDTO.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.product_repository = ProductRepository(db)
        self.gallery_repository = ProductGalleryRepository(db)
        self.variant_repository = ProductVariantRepository(db)
        self.modification_repository = ModificationValueRepository(db)
        self.product_model: ProductEntity | None = None

    async def execute(self, id: int) -> FullProductRDTO:
        """
        Выполняет операцию получения полной информации о товаре по ID.

        Args:
            id (int): Идентификатор товара.

        Returns:
            FullProductRDTO: Объект с полной информацией о товаре.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        await self.validate(id=id)
        return await self.transform(id=id)

    async def validate(self, id: int) -> None:
        """
        Валидирует существование товара с данным ID.

        Args:
            id (int): Идентификатор товара для поиска.

        Raises:
            AppExceptionResponse: Если товар не найден.
        """
        self.product_model = await self.product_repository.get(
            id=id,
            options=self.product_repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.product_model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, id: int) -> FullProductRDTO:
        """
        Преобразует данные в FullProductRDTO.

        Args:
            id (int): Идентификатор товара.

        Returns:
            FullProductRDTO: Объект с полной информацией о товаре.
        """
        # Получаем основную информацию о товаре
        product_dto = ProductWithRelationsRDTO.model_validate(self.product_model)

        # Получаем галерею товара
        gallery_entities = await self.gallery_repository.get_with_filters(
            filters=[ProductGalleryEntity.product_id == id],
            options=self.gallery_repository.default_relationships(),
        )
        galleries_dto = [ProductGalleryWithRelationsRDTO.model_validate(gallery) for gallery in gallery_entities]

        # Получаем варианты товара
        variant_entities = await self.variant_repository.get_with_filters(
            filters=[ProductVariantEntity.product_id == id],
            options=self.variant_repository.default_relationships(),
        )
        variants_dto = [ProductVariantWithRelationsRDTO.model_validate(variant) for variant in variant_entities]

        # Получаем значения модификаций товара
        modification_entities = await self.modification_repository.get_with_filters(
            filters=[ModificationValueEntity.product_id == id],
            options=self.modification_repository.default_relationships(),
        )
        modification_values_dto = [ModificationValueWithRelationsRDTO.model_validate(modification) for modification in modification_entities]

        return FullProductRDTO(
            product=product_dto,
            galleries=galleries_dto,
            variants=variants_dto,
            modification_values=modification_values_dto
        )