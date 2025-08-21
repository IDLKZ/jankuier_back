from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field.field_dto import FieldCDTO, FieldWithRelationsRDTO
from app.adapters.repository.field.field_repository import FieldRepository
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateFieldCase(BaseUseCase[FieldWithRelationsRDTO]):
    """
    Класс Use Case для создания нового поля.

    Использует:
        - Репозиторий `FieldRepository` для работы с базой данных.
        - Репозиторий `CityRepository` для проверки существования города.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `FieldCDTO` для входных данных.
        - DTO `FieldWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldRepository): Репозиторий для работы с полями.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldEntity | None): Созданная модель поля.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldRepository(db)
        self.city_repository = CityRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: FieldEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: FieldCDTO, file: UploadFile | None = None
    ) -> FieldWithRelationsRDTO:
        """
        Выполняет операцию создания поля.

        Args:
            dto (FieldCDTO): Данные для создания поля.
            file (UploadFile | None): Файл изображения поля.

        Returns:
            FieldWithRelationsRDTO: Созданное поле с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: FieldCDTO, file: UploadFile | None = None) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (FieldCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка уникальности value
        if dto.value:
            existed = await self.repository.get_first_with_filters(
                filters=[func.lower(self.repository.model.value) == dto.value.lower()],
                include_deleted_filter=True,
            )
            if existed:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
                )

        # Проверка существования города
        if dto.city_id:
            city = await self.city_repository.get(dto.city_id)
            if not city:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found")
                )

        # Проверка файла изображения
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID
        if dto.image_id:
            image = await self.file_repository.get(dto.image_id)
            if not image:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: FieldCDTO, file: UploadFile | None = None) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (FieldCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Автогенерация value если не указан
        if not dto.value:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Сохранение файла
        if file:
            self.upload_folder = AppFileExtensionConstants.field_image_directory(
                dto.value
            )
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        self.model = FieldEntity(**dto.dict())
