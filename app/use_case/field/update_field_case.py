from fastapi import UploadFile
from sqlalchemy import func, and_
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


class UpdateFieldCase(BaseUseCase[FieldWithRelationsRDTO]):
    """
    Класс Use Case для обновления поля.

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
        model (FieldEntity | None): Обновляемая модель поля.
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
        self, id: int, dto: FieldCDTO, file: UploadFile | None = None
    ) -> FieldWithRelationsRDTO:
        """
        Выполняет операцию обновления поля.

        Args:
            id (int): Идентификатор поля.
            dto (FieldCDTO): Данные для обновления поля.
            file (UploadFile | None): Файл изображения поля.

        Returns:
            FieldWithRelationsRDTO: Обновленное поле с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: FieldCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор поля для проверки.
            dto (FieldCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования поля
        self.model = await self.repository.get(id)
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

        # Проверка уникальности value (исключая текущую запись)
        if dto.value:
            existed = await self.repository.get_first_with_filters(
                filters=[
                    and_(
                        func.lower(self.repository.model.value) == dto.value.lower(),
                        self.repository.model.id != id,
                    )
                ],
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
        if dto.image_id and self.model.image_id != dto.image_id:
            image = await self.file_repository.get(dto.image_id)
            if not image:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(
        self, id: int, dto: FieldCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование входных данных.

        Args:
            id (int): Идентификатор поля.
            dto (FieldCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Автогенерация value если не указан
        if not dto.value:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Обработка файла
        if file:
            self.upload_folder = AppFileExtensionConstants.field_image_directory(dto.value)
            if self.model.image_id:
                # Обновление существующего файла
                file_entity = await self.file_service.update_file(
                    file_id=self.model.image_id,
                    new_file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            else:
                # Создание нового файла
                file_entity = await self.file_service.save_file(
                    file=file,
                    uploaded_folder=self.upload_folder,
                    extensions=self.extensions,
                )
            dto.image_id = file_entity.id