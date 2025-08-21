from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.modification_type.modification_type_dto import (
    ModificationTypeCDTO,
    ModificationTypeRDTO,
)
from app.adapters.repository.modification_type.modification_type_repository import (
    ModificationTypeRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ModificationTypeEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateModificationTypeCase(BaseUseCase[ModificationTypeRDTO]):
    """
    Класс Use Case для создания нового типа модификации.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeCDTO` для входных данных.
        - DTO `ModificationTypeRDTO` для возврата данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (ModificationTypeEntity | None): Модель типа модификации для создания.

    Методы:
        execute(dto: ModificationTypeCDTO) -> ModificationTypeRDTO:
            Выполняет создание типа модификации.
        validate(dto: ModificationTypeCDTO):
            Валидирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)
        self.model: ModificationTypeEntity | None = None

    async def execute(self, dto: ModificationTypeCDTO) -> ModificationTypeRDTO:
        """
        Выполняет операцию создания нового типа модификации.

        Args:
            dto (ModificationTypeCDTO): DTO с данными для создания типа модификации.

        Returns:
            ModificationTypeRDTO: Созданный объект типа модификации.

        Raises:
            AppExceptionResponse: Если тип модификации с таким значением уже существует.
        """
        await self.validate(dto)
        model = await self.repository.create(self.model)
        return ModificationTypeRDTO.from_orm(model)

    async def validate(self, dto: ModificationTypeCDTO) -> None:
        """
        Валидирует данные перед созданием типа модификации.

        Args:
            dto (ModificationTypeCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если тип модификации с таким значением уже существует.
        """
        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )

        # Создание модели для сохранения
        self.model = ModificationTypeEntity(**dto.dict())
