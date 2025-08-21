import json
import re
from decimal import Decimal
from fastapi import UploadFile
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy.academy_dto import (
    AcademyUpdateDTO,
    AcademyWithRelationsRDTO,
)
from app.adapters.repository.academy.academy_repository import AcademyRepository
from app.adapters.repository.city.city_repository import CityRepository
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateAcademyCase(BaseUseCase[AcademyWithRelationsRDTO]):
    """
    Класс Use Case для обновления академии.

    Использует:
        - Репозиторий `AcademyRepository` для работы с базой данных.
        - Репозиторий `CityRepository` для проверки существования города.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyUpdateDTO` для входных данных.
        - DTO `AcademyWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyRepository): Репозиторий для работы с академиями.
        city_repository (CityRepository): Репозиторий для работы с городами.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyEntity | None): Обновляемая модель академии.
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
        self, id: int, dto: AcademyUpdateDTO, file: UploadFile | None = None
    ) -> AcademyWithRelationsRDTO:
        """
        Выполняет операцию обновления академии.

        Args:
            id (int): Идентификатор академии.
            dto (AcademyUpdateDTO): Данные для обновления академии.
            file (UploadFile | None): Новый файл главного изображения академии.

        Returns:
            AcademyWithRelationsRDTO: Обновленная академия с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: AcademyUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор академии.
            dto (AcademyUpdateDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.not_found(
                message=i18n.gettext("academy_not_found")
            )

        # Проверка существования города (если указан для обновления)
        if dto.city_id is not None and dto.city_id:
            city = await self.city_repository.get(dto.city_id)
            if not city:
                raise AppExceptionResponse.bad_request(
                    message=i18n.gettext("city_not_found")
                )

        # Валидация возрастного диапазона
        min_age = dto.min_age if dto.min_age is not None else model.min_age
        max_age = dto.max_age if dto.max_age is not None else model.max_age

        if min_age >= max_age:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("age_range_validation_error")
            )

        # Валидация пола (если обновляется)
        if dto.gender is not None and dto.gender not in [0, 1, 2]:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("gender_validation_error")
            )

        # Валидация рабочего времени (если обновляется)
        if dto.working_time is not None:
            self._validate_working_time_json(dto.working_time)

        # Валидация email (если обновляется)
        if dto.email is not None and dto.email:
            self._validate_email(dto.email)

        # Валидация телефонов (если обновляются)
        if dto.phone is not None and dto.phone:
            self._validate_phone(dto.phone)
        if dto.additional_phone is not None and dto.additional_phone:
            self._validate_phone(dto.additional_phone)

        # Валидация средней цены (если обновляется)
        if dto.average_price is not None and dto.average_price <= Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("average_price_validation_error")
            )

        # Валидация времени тренировки (если обновляется)
        if (
            dto.average_training_time_in_minute is not None
            and dto.average_training_time_in_minute <= 0
        ):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("training_time_validation_error")
            )

        # Проверка нового файла изображения (если загружается)
        if file:
            self.file_service.validate_file(file, self.extensions)

        # Проверка существования файла изображения по ID (если обновляется)
        if dto.image_id is not None and dto.image_id:
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
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
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
        phone_pattern = r"^[\+]?[0-9\s\-\(\)]{7,20}$"
        if not re.match(phone_pattern, phone):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("invalid_phone_format")
            )

    async def transform(
        self, id: int, dto: AcademyUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор академии.
            dto (AcademyUpdateDTO): Данные для преобразования.
            file (UploadFile | None): Файл для сохранения.
        """
        self.model = await self.repository.get(id)

        # Обработка нового файла изображения
        if file:
            # Удаление старого файла (если есть)
            if self.model.image_id:
                await self.file_service.delete_file(file_id=self.model.image_id)

            # Определяем папку для загрузки
            value = self.model.value if self.model.value else str(id)
            self.upload_folder = f"academies/images/{value}"

            # Сохраняем новый файл
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id
