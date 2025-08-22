from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialWithRelationsRDTO,
)
from app.adapters.repository.academy_material.academy_material_repository import (
    AcademyMaterialRepository,
)
from app.core.app_exception_response import AppExceptionResponse
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetAcademyMaterialByIdCase(BaseUseCase[AcademyMaterialWithRelationsRDTO]):
    """
    Класс Use Case для получения материала академии по ID.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - DTO `AcademyMaterialWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.

    Методы:
        execute(id: int) -> AcademyMaterialWithRelationsRDTO:
            Выполняет запрос и возвращает материал академии по ID.
        validate(id: int):
            Валидация входных параметров.
        transform():
            Преобразование данных (не используется в данном случае).
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyMaterialRepository(db)

    async def execute(self, id: int) -> AcademyMaterialWithRelationsRDTO:
        """
        Выполняет операцию получения материала академии по ID.

        Args:
            id (int): Уникальный идентификатор материала академии.

        Returns:
            AcademyMaterialWithRelationsRDTO: Материал академии с связями.

        Raises:
            AppExceptionResponse: Если материал не найден.
        """
        await self.validate(id)

        model = await self.repository.get(
            id, 
            include_deleted_filter=True,
            options=self.repository.default_relationships()
        )
        
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("academy_material_not_found")
            )

        return AcademyMaterialWithRelationsRDTO.from_orm(model)

    async def validate(self, id: int) -> None:
        """
        Валидация входных параметров.

        Args:
            id (int): ID для валидации.

        Raises:
            AppExceptionResponse: Если ID некорректный.
        """
        if not id or id <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_id")
            )

    async def transform(self) -> None:
        """
        Преобразование данных (не используется в данном случае).
        """
        pass