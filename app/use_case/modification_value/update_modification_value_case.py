from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_value.modification_value_dto import ModificationValueUpdateDTO, ModificationValueWithRelationsRDTO
from app.adapters.repository.modification_type.modification_type_repository import ModificationTypeRepository
from app.adapters.repository.modification_value.modification_value_repository import ModificationValueRepository
from app.adapters.repository.product.product_repository import ProductRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationValueEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class UpdateModificationValueCase(BaseUseCase[ModificationValueWithRelationsRDTO]):
    """
    Класс Use Case для обновления значения модификации.

    Использует:
        - Репозиторий `ModificationValueRepository` для работы с базой данных.
        - DTO `ModificationValueUpdateDTO` для входных данных.
        - DTO `ModificationValueWithRelationsRDTO` для возврата данных с отношениями.

    Атрибуты:
        repository (ModificationValueRepository): Репозиторий для работы со значениями модификаций.
        modification_type_repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        product_repository (ProductRepository): Репозиторий для работы с товарами.
        model (ModificationValueEntity | None): Модель значения модификации для обновления.

    Методы:
        execute(id: int, dto: ModificationValueUpdateDTO) -> ModificationValueWithRelationsRDTO:
            Выполняет обновление значения модификации.
        validate(id: int, dto: ModificationValueUpdateDTO):
            Валидирует данные перед обновлением.
        transform(dto: ModificationValueUpdateDTO):
            Трансформирует данные перед обновлением.
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

    async def execute(self, id: int, dto: ModificationValueUpdateDTO) -> ModificationValueWithRelationsRDTO:
        """
        Выполняет операцию обновления значения модификации.

        Args:
            id (int): Идентификатор значения модификации для обновления.
            dto (ModificationValueUpdateDTO): DTO с данными для обновления значения модификации.

        Returns:
            ModificationValueWithRelationsRDTO: Обновленный объект значения модификации с отношениями.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено, связанные сущности не найдены или валидация не прошла.
        """
        await self.validate(id=id, dto=dto)
        await self.transform(dto=dto)
        self.model = await self.repository.update(obj=self.model, dto=dto)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return ModificationValueWithRelationsRDTO.from_orm(self.model)

    async def validate(self, id: int, dto: ModificationValueUpdateDTO) -> None:
        """
        Валидирует данные перед обновлением значения модификации.

        Args:
            id (int): Идентификатор значения модификации для обновления.
            dto (ModificationValueUpdateDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если значение модификации не найдено или связанные сущности не найдены.
        """
        # Проверка существования значения модификации
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self, dto: ModificationValueUpdateDTO):
        """
        Трансформирует данные перед обновлением значения модификации.

        Args:
            dto (ModificationValueUpdateDTO): DTO с данными для трансформации.
        """
        # Трансформация не требуется для этой простой сущности
        pass