from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_material.academy_material_dto import (
    AcademyMaterialUpdateDTO,
    AcademyMaterialWithRelationsRDTO,
)
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


class UpdateAcademyMaterialCase(BaseUseCase[AcademyMaterialWithRelationsRDTO]):
    """
    Класс Use Case для обновления материала академии.

    Использует:
        - Репозиторий `AcademyMaterialRepository` для работы с базой данных.
        - Репозиторий `AcademyGroupRepository` для проверки существования группы.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyMaterialUpdateDTO` для входных данных.
        - DTO `AcademyMaterialWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyMaterialRepository): Репозиторий для работы с материалами академий.
        group_repository (AcademyGroupRepository): Репозиторий для работы с группами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyMaterialEntity | None): Обновляемая модель материала.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyMaterialRepository(db)
        self.group_repository = AcademyGroupRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyMaterialEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.ALL_EXTENSIONS

    async def execute(
        self, id: int, dto: AcademyMaterialUpdateDTO, file: UploadFile | None = None
    ) -> AcademyMaterialWithRelationsRDTO:
        """
        Выполняет операцию обновления материала академии.

        Args:
            id (int): Идентификатор материала академии.
            dto (AcademyMaterialUpdateDTO): Данные для обновления материала.
            file (UploadFile | None): Новый файл материала.

        Returns:
            AcademyMaterialWithRelationsRDTO: Обновленный материал академии с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyMaterialWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: AcademyMaterialUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор материала академии.
            dto (AcademyMaterialUpdateDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования материала академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_material_not_found")
            )

        # Проверка существования новой группы (если изменяется)
        if dto.group_id is not None:
            if dto.group_id:  # Если не None и не 0
                group = await self.group_repository.get(dto.group_id)
                if not group:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("academy_group_not_found")
                    )

                # Проверка, что группа принадлежит той же академии
                if group.academy_id != model.academy_id:
                    raise AppExceptionResponse.bad_request(
                        message=i18n.gettext("academy_group_not_belongs_to_academy")
                    )

        # Проверка нового файла материала (если загружается)
        if file:
            # Валидация типа и размера файла
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования нового файла по ID (если обновляется)
        if dto.file_id is not None and dto.file_id:
            existing_file = await self.file_repository.get(dto.file_id)
            if not existing_file:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found")
                )

        # Проверка дублирования по названию в рамках академии и группы (если название изменяется)
        if dto.title is not None:
            target_group_id = (
                dto.group_id if dto.group_id is not None else model.group_id
            )
            
            duplicate_filters = [
                self.repository.model.academy_id == model.academy_id,
                self.repository.model.title == dto.title,
                self.repository.model.id != id,  # Исключаем текущую запись
            ]
            
            if target_group_id:
                duplicate_filters.append(self.repository.model.group_id == target_group_id)
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
        self, id: int, dto: AcademyMaterialUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор материала академии.
            dto (AcademyMaterialUpdateDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        self.model = await self.repository.get(id)

        # Обработка нового файла материала
        if file:
            # Удаление старого файла (если есть)
            if self.model.file_id:
                await self.file_service.delete_file(file_id=self.model.file_id)

            # Определяем папку для загрузки на основе академии и группы
            academy_value = (
                self.model.academy.value
                if self.model.academy.value
                else str(self.model.academy_id)
            )

            # Определяем группу для папки (берем обновленную или текущую)
            target_group_id = (
                dto.group_id if dto.group_id is not None else self.model.group_id
            )

            if target_group_id:
                group = await self.group_repository.get(target_group_id)
                group_value = group.value if group.value else str(target_group_id)
                self.upload_folder = f"academy_materials/{academy_value}/groups/{group_value}"
            else:
                self.upload_folder = f"academy_materials/{academy_value}"

            # Сохраняем новый файл
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.file_id = file_entity.id