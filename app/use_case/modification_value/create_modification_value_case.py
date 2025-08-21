from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_value.modification_value_dto import (
    ModificationValueCDTO,
    ModificationValueWithRelationsRDTO,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.adapters.repository.modification_value.modification_value_repository import (
    ModificationValueRepository,
)
from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationValueEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class CreateModificationValueCase(BaseUseCase[ModificationValueWithRelationsRDTO]):
    """
    Класс Use Case для создания нового значения модификации.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.
        - DTO `ModificationValueCDTO` для входных данных.
        - DTO `ModificationValueWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.
        modification_type_repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        model (ModificationValueEntity | None): Модель значения модификации для создания.

    Методы:
        execute(dto: ModificationValueCDTO) -> ModificationValueWithRelationsRDTO:
            Выполняет создание значения модификации.
        validate(dto: ModificationValueCDTO):
            Валидирует данные перед созданием.
        transform(dto: ModificationValueCDTO):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationValueRepository(db)
        self.modification_type_repository = ModificationTypeRepository(db)
        self.product_repository = ProductRepository(db)
        self.model: ModificationValueEntity | None = None

    async def execute(
        self, dto: ModificationValueCDTO
    ) -> ModificationValueWithRelationsRDTO:
        """
        Выполняет операцию создания нового значения модификации.

        Args:
            dto (ModificationValueCDTO): DTO с данными для создания значения модификации.

        Returns:
            ModificationValueWithRelationsRDTO: Созданный объект значения модификации с отношениями.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ModificationValueWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: ModificationValueCDTO) -> None:
        """
        Валидирует данные перед созданием значения модификации.

        Args:
            dto (ModificationValueCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если связанные сущности не найдены.
        """
        # Проверка существования типа модификации
        if (
            await self.modification_type_repository.get(dto.modification_type_id)
        ) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("modification_type_not_found_by_id")
            )

        # Проверка существования товара
        if (await self.product_repository.get(dto.product_id)) is None:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("product_not_found_by_id")
            )

    async def transform(self, dto: ModificationValueCDTO):
        """
        Трансформирует данные перед созданием значения модификации.

        Args:
            dto (ModificationValueCDTO): DTO с данными для трансформации.
        """
        # Создание модели для сохранения
        self.model = ModificationValueEntity(**dto.dict())
