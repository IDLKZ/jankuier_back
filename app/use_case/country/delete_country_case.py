from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repository.country.country_repository import CountryRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import CountryEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class DeleteCountryByIdCase(BaseUseCase[bool]):
    """
    Класс Use Case для удаления страны по ID.

    Использует:
        - Репозиторий `CountryRepository` для работы с базой данных.

    Атрибуты:
        repository (CountryRepository): Репозиторий для работы со странами.
        model (CountryEntity | None): Удаляемая модель страны.

    Методы:
        execute(id: int, force_delete: bool = False) -> bool:
            Удаляет страну и возвращает результат операции.
        validate(id: int):
            Проверяет существование страны.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = CountryRepository(db)
        self.model: CountryEntity | None = None

    async def execute(self, id: int, force_delete: bool = False) -> bool:
        """
        Выполняет операцию удаления страны.

        Args:
            id (int): Идентификатор страны.
            force_delete (bool): Принудительное удаление (по умолчанию False - мягкое удаление).

        Returns:
            bool: True если удаление прошло успешно.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        await self.validate(id=id)
        result = await self.repository.delete(id=id, force_delete=force_delete)
        return result

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор страны для проверки.

        Raises:
            AppExceptionResponse: Если страна не найдена.
        """
        self.model = await self.repository.get(id, include_deleted_filter=True)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))