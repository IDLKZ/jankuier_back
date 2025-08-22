from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialCDTO,
    AcademyMaterialWithRelationsRDTO,
)
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.adapters.repository.academy_material.academy_material_repository import (
    AcademyMaterialRepository,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyMaterialEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class CreateAcademyMaterialCase(BaseUseCase[AcademyMaterialWithRelationsRDTO]):
    """
    Класс Use Case для создания нового материала академии.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - Репозиторий `AcademyRepository` для проверки существования академии.
        - Репозиторий `AcademyGroupRepository` для проверки существования группы.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyMaterialCDTO` для входных данных.
        - DTO `AcademyMaterialWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.
        academy_repository (AcademyRepository): Репозиторий для работы с академиями.
        group_repository (AcademyGroupRepository): Репозиторий для работы с группами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyMaterialEntity | None): Созданная модель материала.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyMaterialRepository(db)
        self.academy_repository = AcademyRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyMaterialEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.ALL_EXTENSIONS

    async def execute(
        self, dto: AcademyMaterialCDTO, file: UploadFile | None = None
    ) -> AcademyMaterialWithRelationsRDTO:
        """
        Выполняет операцию создания материала академии.

        Args:
            dto (AcademyMaterialCDTO): Данные для создания материала.
            file (UploadFile | None): Файл материала.

        Returns:
            AcademyMaterialWithRelationsRDTO: Созданный материал академии с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyMaterialWithRelationsRDTO.from_orm(model)

    async def validate(
        self, dto: AcademyMaterialCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (AcademyMaterialCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования академии
        academy = await self.academy_repository.get(dto.academy_id)
        if not academy:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_not_found")
            )

        # Проверка существования группы (если указана)
        if dto.group_id:
            group = await self.group_repository.get(dto.group_id)
            if not group:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("academy_group_not_found")
                )

            # Проверка, что группа принадлежит указанной академии
            if group.academy_id != dto.academy_id:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("academy_group_not_belongs_to_academy")
                )

        # Проверка файла материала (если загружается)
        if file:
            # Валидация типа и размера файла
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по ID (если указан)
        if dto.file_id:
            existing_file = await self.file_repository.get(dto.file_id)
            if not existing_file:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found")
                )

        # Проверка дублирования по названию в рамках академии и группы
        duplicate_filters = [
            self.repository.model.academy_id == dto.academy_id,
            self.repository.model.title == dto.title,
        ]
        
        if dto.group_id:
            duplicate_filters.append(self.repository.model.group_id == dto.group_id)
        else:
            duplicate_filters.append(self.repository.model.group_id.is_(None))

        duplicate_material = await self.repository.get_first_with_filters(
            filters=duplicate_filters
        )
        if duplicate_material:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_material_title_already_exists")
            )

    async def transform(
        self, dto: AcademyMaterialCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (AcademyMaterialCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Сохранение файла материала (если загружается новый)
        if file:
            # Получаем академию для определения папки загрузки
            academy = await self.academy_repository.get(dto.academy_id)
            academy_value = academy.value if academy.value else str(dto.academy_id)

            if dto.group_id:
                # Если указана группа, сохраняем в папку группы
                group = await self.group_repository.get(dto.group_id)
                group_value = group.value if group.value else str(dto.group_id)
                self.upload_folder = f"academy_materials/{academy_value}/groups/{group_value}"
            else:
                # Иначе сохраняем в общую папку академии
                self.upload_folder = f"academy_materials/{academy_value}"

            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id

        self.model = AcademyMaterialEntity(**dto.dict())