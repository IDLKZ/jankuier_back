from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import GetFullAcademyDTO, AcademyWithRelationsRDTO
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.adapters.repository.academy_gallery.academy_gallery_repository import AcademyGalleryRepository
from app.adapters.repository.academy_group.academy_group_repository import AcademyGroupRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyEntity
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase


class GetFullAcademyByIdCase(BaseUseCase[GetFullAcademyDTO]):
    """
    Класс Use Case для получения полной информации об академии по ID.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных академий.
        - Репозиторий `AcademyGalleryRepository` для работы с галереей академии.
        - Репозиторий `AcademyGroupRepository` для работы с группами академии.
        - DTO `GetFullAcademyDTO` для возврата полных данных академии.

    Атрибуты:
        academy_repository (AcademyRepository): Репозиторий для работы с академиями.
        gallery_repository (AcademyGalleryRepository): Репозиторий для работы с галереей.
        group_repository (AcademyGroupRepository): Репозиторий для работы с группами.
        academy_model (AcademyEntity | None): Найденная модель академии.

    Методы:
        execute(id: int) -> GetFullAcademyDTO:
            Выполняет поиск академии по ID и возвращает полную информацию.
        validate(id: int):
            Проверяет существование академии с указанным ID.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.academy_repository = AcademyRepository(db)
        self.gallery_repository = AcademyGalleryRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.academy_model: AcademyEntity | None = None

    async def execute(self, id: int) -> GetFullAcademyDTO:
        """
        Выполняет операцию получения полной информации об академии по ID.

        Args:
            id (int): Идентификатор академии.

        Returns:
            GetFullAcademyDTO: Полная информация об академии с галереями и группами.

        Raises:
            AppExceptionResponse: Если академия не найдена.
        """
        await self.validate(id=id)

        # Получаем основную информацию об академии
        academy_dto = AcademyWithRelationsRDTO.from_orm(self.academy_model)

        # Получаем галереи академии
        galleries = await self.gallery_repository.get_all(
            filters=[self.gallery_repository.model.academy_id == id],
            options=self.gallery_repository.default_relationships(),
            include_deleted_filter=False
        )

        # Получаем группы академии
        groups = await self.group_repository.get_all(
            filters=[self.group_repository.model.academy_id == id],
            options=self.group_repository.default_relationships(),
            include_deleted_filter=False
        )

        # Конвертируем в DTO
        from app.adapters.dto.academy_gallery.academy_gallery_dto import AcademyGalleryWithRelationsRDTO
        from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupWithRelationsRDTO

        gallery_dtos = [AcademyGalleryWithRelationsRDTO.from_orm(gallery) for gallery in galleries]
        group_dtos = [AcademyGroupWithRelationsRDTO.from_orm(group) for group in groups]

        return GetFullAcademyDTO(
            academy=academy_dto,
            galleries=gallery_dtos,
            groups=group_dtos
        )

    async def validate(self, id: int) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор академии для проверки.

        Raises:
            AppExceptionResponse: Если академия не найдена.
        """
        self.academy_model = await self.academy_repository.get(
            id,
            options=self.academy_repository.default_relationships(),
            include_deleted_filter=True,
        )
        if not self.academy_model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))