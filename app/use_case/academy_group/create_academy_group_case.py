from decimal import Decimal
from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupCDTO, AcademyGroupWithRelationsRDTO
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.adapters.repository.academy_group.academy_group_repository import AcademyGroupRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateAcademyGroupCase(BaseUseCase[AcademyGroupWithRelationsRDTO]):
    """
    Класс Use Case для создания новой группы академии.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - Репозиторий `AcademyRepository` для проверки существования академии.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyGroupCDTO` для входных данных.
        - DTO `AcademyGroupWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.
        academy_repository (AcademyRepository): Репозиторий для работы с академиями.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyGroupEntity | None): Созданная модель группы академии.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupRepository(db)
        self.academy_repository = AcademyRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyGroupEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: AcademyGroupCDTO, file: UploadFile | None = None
    ) -> AcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию создания группы академии.

        Args:
            dto (AcademyGroupCDTO): Данные для создания группы академии.
            file (UploadFile | None): Файл главного изображения группы.

        Returns:
            AcademyGroupWithRelationsRDTO: Созданная группа академии с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: AcademyGroupCDTO, file: UploadFile | None = None) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (AcademyGroupCDTO): Данные для валидации.
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

        # Проверка уникальности value
        if dto.value:
            existed = await self.repository.get_first_with_filters(
                filters=[func.lower(self.repository.model.value) == dto.value.lower()],
                include_deleted_filter=True,
            )
            if existed:
                raise AppExceptionResponse.bad_request(
                    message=f"{i18n.gettext('the_next_value_already_exists')}: {dto.value}"
                )

        # Проверка обязательности названия группы
        if not dto.name or not dto.name.strip():
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_name_required")
            )

        # Валидация возрастного диапазона
        if dto.min_age >= dto.max_age:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("age_range_validation_error")
            )

        # Валидация пола
        if dto.gender not in [0, 1, 2]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("gender_validation_error")
            )

        # Валидация количества мест
        if dto.booked_space > dto.free_space:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("group_space_validation_error")
            )

        # Валидация цены (если указана)
        if dto.price is not None and dto.price <= Decimal('0'):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("average_price_validation_error")
            )

        # Валидация описания цены (если цена указана, нужно хотя бы одно описание)
        if dto.price is not None and not any([dto.price_per_ru, dto.price_per_kk, dto.price_per_en]):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("price_per_validation_error")
            )

        # Валидация времени тренировки (если указано)
        if dto.average_training_time_in_minute is not None and dto.average_training_time_in_minute <= 0:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("training_time_validation_error")
            )

        # Проверка файла изображения (если загружается)
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID (если указан)
        if dto.image_id:
            image = await self.file_repository.get(dto.image_id)
            if not image:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("file_not_found")
                )

    async def transform(self, dto: AcademyGroupCDTO, file: UploadFile | None = None) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (AcademyGroupCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Автогенерация value если не указан
        if not dto.value:
            dto.value = DbValueConstants.get_value(dto.name)

        # Сохранение файла изображения
        if file:
            self.upload_folder = f"{AppFileExtensionConstants.FieldFolderName}/academy_groups/{dto.value}"
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        self.model = AcademyGroupEntity(**dto.dict())