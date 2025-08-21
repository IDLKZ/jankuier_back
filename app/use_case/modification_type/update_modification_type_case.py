from sqlalchemy import and_
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


class UpdateModificationTypeCase(BaseUseCase[ModificationTypeRDTO]):
    """
    Класс Use Case для обновления типа модификации.

    Использует:
        - Репозиторий `ModificationTypeRepository` для работы с базой данных.
        - DTO `ModificationTypeCDTO` для входных данных.
        - DTO `ModificationTypeRDTO` для возврата данных.

    Атрибуты:
        repository (ModificationTypeRepository): Репозиторий для работы с типами модификаций.
        model (ModificationTypeEntity | None): Модель типа модификации для обновления.

    Методы:
        execute(id: int, dto: ModificationTypeCDTO) -> ModificationTypeRDTO:
            Выполняет обновление типа модификации.
        validate(id: int, dto: ModificationTypeCDTO):
            Валидирует данные перед обновлением.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = ModificationTypeRepository(db)
        self.model: ModificationTypeEntity | None = None

    async def execute(self, id: int, dto: ModificationTypeCDTO) -> ModificationTypeRDTO:
        """
        Выполняет операцию обновления типа модификации.

        Args:
            id (int): Идентификатор типа модификации.
            dto (ModificationTypeCDTO): DTO с данными для обновления.

        Returns:
            ModificationTypeRDTO: Обновленный объект типа модификации.

        Raises:
            AppExceptionResponse: Если тип модификации не найден или значение уже существует.
        """
        await self.validate(id=id, dto=dto)
        model = await self.repository.update(obj=self.model, dto=dto)
        return ModificationTypeRDTO.from_orm(model)

    async def validate(self, id: int, dto: ModificationTypeCDTO) -> None:
        """
        Валидирует данные перед обновлением типа модификации.

        Args:
            id (int): Идентификатор типа модификации.
            dto (ModificationTypeCDTO): DTO с данными для валидации.

        Raises:
            AppExceptionResponse: Если тип модификации не найден или значение уже существует.
        """
        # Проверка существования типа модификации
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Автогенерация value из title_ru если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Проверка уникальности значения (исключая текущую запись)
        existed = await self.repository.get_first_with_filters(
            filters=[
                and_(
                    self.repository.model.id != id,
                    self.repository.model.value == dto.value,
                )
            ],
            include_deleted_filter=True,
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )
