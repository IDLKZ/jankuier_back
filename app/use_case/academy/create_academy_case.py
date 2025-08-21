import json
import re
from decimal import Decimal
from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import AcademyCDTO, AcademyWithRelationsRDTO
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.shared.db_value_constants import DbValueConstants
from app.use_case.base_case import BaseUseCase


class CreateAcademyCase(BaseUseCase[AcademyWithRelationsRDTO]):
    """
    Класс Use Case для создания новой академии.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - Репозиторий `CityRepository` для проверки существования города.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyCDTO` для входных данных.
        - DTO `AcademyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyEntity | None): Созданная модель академии.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyRepository(db)
        self.city_repository = CityRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, dto: AcademyCDTO, file: UploadFile | None = None
    ) -> AcademyWithRelationsRDTO:
        """
        Выполняет операцию создания академии.

        Args:
            dto (AcademyCDTO): Данные для создания академии.
            file (UploadFile | None): Файл главного изображения академии.

        Returns:
            AcademyWithRelationsRDTO: Созданная академия с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(dto=dto, file=file)
        await self.transform(dto=dto, file=file)
        model = await self.repository.create(self.model)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyWithRelationsRDTO.from_orm(model)

    async def validate(self, dto: AcademyCDTO, file: UploadFile | None = None) -> None:
        """
        Валидация перед выполнением.

        Args:
            dto (AcademyCDTO): Данные для валидации.
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
                    message=f"{i18n.gettext('the_next_value_already_exists')}: {dto.value}"
                )

        # Проверка существования города (если указан)
        if dto.city_id:
            city = await self.city_repository.get(dto.city_id)
            if not city:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found")
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

        # Валидация рабочего времени (JSON)
        if dto.working_time:
            self._validate_working_time_json(dto.working_time)

        # Валидация email (если указан)
        if dto.email:
            self._validate_email(dto.email)

        # Валидация телефонов (если указаны)
        if dto.phone:
            self._validate_phone(dto.phone)
        if dto.additional_phone:
            self._validate_phone(dto.additional_phone)

        # Валидация средней цены (если указана)
        if dto.average_price is not None and dto.average_price <= Decimal('0'):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("average_price_validation_error")
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

    def _validate_working_time_json(self, working_time: any) -> None:
        """
        Валидация JSON данных рабочего времени.

        Args:
            working_time: JSON данные рабочего времени.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        try:
            if isinstance(working_time, str):
                json.loads(working_time)
            elif not isinstance(working_time, (dict, list)):
                raise ValueError("Invalid JSON format")
        except (json.JSONDecodeError, ValueError):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("working_time_validation_error")
            )

    def _validate_email(self, email: str) -> None:
        """
        Валидация email адреса.

        Args:
            email (str): Email для валидации.

        Raises:
            AppExceptionResponse: Если email невалиден.
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_email_format")
            )

    def _validate_phone(self, phone: str) -> None:
        """
        Валидация номера телефона.

        Args:
            phone (str): Телефон для валидации.

        Raises:
            AppExceptionResponse: Если телефон невалиден.
        """
        # Простая валидация телефона (только цифры, +, -, (, ), пробелы)
        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{7,20}$'
        if not re.match(phone_pattern, phone):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_phone_format")
            )

    async def transform(self, dto: AcademyCDTO, file: UploadFile | None = None) -> None:
        """
        Преобразование DTO в модель.

        Args:
            dto (AcademyCDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        # Автогенерация value если не указан
        if not dto.value:
            dto.value = DbValueConstants.get_value(dto.title_ru)

        # Сохранение файла изображения
        if file:
            self.upload_folder = f"academies/images/{dto.value}"
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id

        self.model = AcademyEntity(**dto.dict())