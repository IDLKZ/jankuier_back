from fastapi import UploadFile
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.field_party.field_party_dto import (
    FieldPartyCDTO,
    FieldPartyWithRelationsRDTO,
)
from app.adapters.repository.field_party.field_party_repository import (
    FieldPartyRepository,
)
from app.adapters.repository.field.field_repository import FieldRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import FieldPartyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class UpdateFieldPartyCase(BaseUseCase[FieldPartyWithRelationsRDTO]):
    """
    Класс Use Case для обновления площадки поля.

    Использует:
        - Репозиторий `FieldPartyRepository` для работы с базой данных.
        - Репозиторий `FieldRepository` для проверки существования поля.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `FieldPartyCDTO` для входных данных.
        - DTO `FieldPartyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (FieldPartyRepository): Репозиторий для работы с площадками полей.
        field_repository (FieldRepository): Репозиторий для работы с полями.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (FieldPartyEntity | None): Обновляемая модель площадки поля.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = FieldPartyRepository(db)
        self.field_repository = FieldRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: FieldPartyEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, dto: FieldPartyCDTO, file: UploadFile | None = None
    ) -> FieldPartyWithRelationsRDTO:
        """
        Выполняет операцию обновления площадки поля.

        Args:
            id (int): Идентификатор площадки поля.
            dto (FieldPartyCDTO): Данные для обновления площадки поля.
            file (UploadFile | None): Файл изображения площадки.

        Returns:
            FieldPartyWithRelationsRDTO: Обновленная площадка поля с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return FieldPartyWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: FieldPartyCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор площадки поля для проверки.
            dto (FieldPartyCDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования площадки поля
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

        # Проверка существования поля
        field = await self.field_repository.get(dto.field_id)
        if not field:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("field_not_found")
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
        self, id: int, dto: FieldPartyCDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование входных данных.

        Args:
            id (int): Идентификатор площадки поля.
            dto (FieldPartyCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Автогенерация value если не указан
        if not dto.value:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Обработка файла
        if file:
            self.upload_folder = AppFileExtensionConstants.field_party_image_directory(
                dto.value
            )
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
