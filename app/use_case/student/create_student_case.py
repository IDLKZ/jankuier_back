from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.student.student_dto import StudentCDTO, StudentWithRelationsRDTO
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.adapters.repository.student.student_repository import StudentRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import StudentEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateStudentCase(BaseUseCase[StudentWithRelationsRDTO]):
    """
    Класс Use Case для создания нового студента.

    Использует:
        - Репозиторий `StudentRepository` для работы с базой данных.
        - DTO `StudentCDTO` для входных данных.
        - DTO `StudentWithRelationsRDTO` для возврата данных с отношениями.
        - `FileService` для работы с фотографиями.

    Атрибуты:
        repository (StudentRepository): Репозиторий для работы со студентами.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (StudentEntity | None): Модель студента для создания.

    Методы:
        execute(dto: StudentCDTO, file: UploadFile | None = None) -> StudentWithRelationsRDTO:
            Выполняет создание студента.
        validate(dto: StudentCDTO, file: UploadFile | None = None):
            Валидирует данные перед созданием.
        transform(dto: StudentCDTO, file: UploadFile | None = None):
            Трансформирует данные перед созданием.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = StudentRepository(db)
        self.city_repository = CityRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: StudentEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: StudentCDTO, file: UploadFile | None = None
    ) -> StudentWithRelationsRDTO:
        """
        Выполняет операцию создания нового студента.

        Args:
            dto (StudentCDTO): DTO с данными для создания студента.
            file (UploadFile | None): Опциональный файл фотографии студента.

        Returns:
            StudentWithRelationsRDTO: Созданный объект студента с отношениями.

        Raises:
            AppExceptionResponse: Если студент с таким значением уже существует или валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        self.model = await self.repository.create(obj=self.model)
        self.model = await self.repository.get(
            id=self.model.id, options=self.repository.default_relationships()
        )
        return StudentWithRelationsRDTO.from_orm(self.model)

    async def validate(self, dto: StudentCDTO, file: UploadFile | None = None) -> None:
        """
        Валидирует данные перед созданием студента.

        Args:
            dto (StudentCDTO): DTO с данными для валидации.
            file (UploadFile | None): Опциональный файл фотографии для валидации.

        Raises:
            AppExceptionResponse: Если студент с таким значением уже существует, связанные сущности не найдены или файл не валиден.
        """
        # Автогенерация value из first_name если не предоставлено
        if dto.value is None:
            dto.value = DbValueConstants.get_value(dto.first_name)

        # Проверка уникальности value
        existed = await self.repository.get_first_with_filters(
            filters=[self.repository.model.value == dto.value]
        )
        if existed:
            raise AppExceptionResponse.bad_request(
                message=f"{i18n.gettext('the_next_value_already_exists')}{dto.value}"
            )

        # Проверка существования города (если указан)
        if dto.city_id:
            if (await self.city_repository.get(dto.city_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found_by_id")
                )

        # Валидация файла фотографии
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла по image_id
        if dto.image_id:
            if (await self.file_repository.get(dto.image_id)) is None:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("image_not_found_by_id")
                )

    async def transform(self, dto: StudentCDTO, file: UploadFile | None = None):
        """
        Трансформирует данные перед созданием студента.

        Args:
            dto (StudentCDTO): DTO с данными для трансформации.
            file (UploadFile | None): Опциональный файл фотографии для сохранения.
        """
        # Определение папки для загрузки фотографий студентов
        self.upload_folder = f"students/photos/{dto.value}"

        # Сохранение файла если предоставлен
        if file:
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        # Создание модели для сохранения
        self.model = StudentEntity(**dto.dict())
