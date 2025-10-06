from decimal import Decimal
from fastapi import UploadFile
from sqlalchemy import func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.dto.academy_group.academy_group_dto import (
    AcademyGroupUpdateDTO,
    AcademyGroupWithRelationsRDTO,
)
from app.adapters.repository.academy_group.academy_group_repository import (
    AcademyGroupRepository,
)
from app.adapters.repository.file.file_repository import FileRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import AcademyGroupEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.service.file_service import FileService
from app.shared.app_file_constants import AppFileExtensionConstants
from app.use_case.base_case import BaseUseCase


class UpdateAcademyGroupCase(BaseUseCase[AcademyGroupWithRelationsRDTO]):
    """
    Класс Use Case для обновления группы академии.

    Использует:
        - Репозиторий `AcademyGroupRepository` для работы с базой данных.
        - Репозиторий `FileRepository` для проверки существования файла.
        - Сервис `FileService` для работы с файлами.
        - DTO `AcademyGroupUpdateDTO` для входных данных.
        - DTO `AcademyGroupWithRelationsRDTO` для возврата данных с связями.

    Атрибуты:
        repository (AcademyGroupRepository): Репозиторий для работы с группами академий.
        file_repository (FileRepository): Репозиторий для работы с файлами.
        file_service (FileService): Сервис для работы с файлами.
        model (AcademyGroupEntity | None): Обновляемая модель группы академии.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация Use Case.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
        """
        self.repository = AcademyGroupRepository(db)
        self.file_repository = FileRepository(db)
        self.file_service = FileService(db)
        self.model: AcademyGroupEntity | None = None
        self.upload_folder: str | None = None
        self.extensions = AppFileExtensionConstants.IMAGE_EXTENSIONS

    async def execute(
        self, id: int, dto: AcademyGroupUpdateDTO, file: UploadFile | None = None
    ) -> AcademyGroupWithRelationsRDTO:
        """
        Выполняет операцию обновления группы академии.

        Args:
            id (int): Идентификатор группы академии.
            dto (AcademyGroupUpdateDTO): Данные для обновления группы академии.
            file (UploadFile | None): Новый файл главного изображения группы.

        Returns:
            AcademyGroupWithRelationsRDTO: Обновленная группа академии с связями.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        await self.validate(id=id, dto=dto, file=file)
        await self.transform(id=id, dto=dto, file=file)
        model = await self.repository.update(obj=self.model, dto=dto)
        model = await self.repository.get(
            model.id, options=self.repository.default_relationships()
        )
        return AcademyGroupWithRelationsRDTO.from_orm(model)

    async def validate(
        self, id: int, dto: AcademyGroupUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Валидация перед выполнением.

        Args:
            id (int): Идентификатор группы академии.
            dto (AcademyGroupUpdateDTO): Данные для валидации.
            file (UploadFile | None): Файл для валидации.

        Raises:
            AppExceptionResponse: Если валидация не прошла.
        """
        # Проверка существования группы академии
        model = await self.repository.get(id, include_deleted_filter=True)
        if not model:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("academy_group_not_found")
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

        # Валидация количества мест
        booked_space = (
            dto.booked_space if dto.booked_space is not None else model.booked_space
        )
        free_space = dto.free_space if dto.free_space is not None else model.free_space

        if booked_space > free_space:
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("group_space_validation_error")
            )

        # Валидация цены (если обновляется)
        if dto.price is not None and dto.price <= Decimal("0"):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("average_price_validation_error")
            )

        # Валидация описания цены (если цена указана, нужно хотя бы одно описание)
        price = dto.price if dto.price is not None else model.price
        price_per_ru = (
            dto.price_per_ru if dto.price_per_ru is not None else model.price_per_ru
        )
        price_per_kk = (
            dto.price_per_kk if dto.price_per_kk is not None else model.price_per_kk
        )
        price_per_en = (
            dto.price_per_en if dto.price_per_en is not None else model.price_per_en
        )

        if price is not None and not any([price_per_ru, price_per_kk, price_per_en]):
            raise AppExceptionResponse.bad_request(
                message=i18n.gettext("price_per_validation_error")
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

        # Валидация бизнес-правил для обновления статуса набора
        if dto.is_recruiting is not None and model.is_recruiting != dto.is_recruiting:
            # Проверяем, есть ли активные студенты в группе
            # (Это можно реализовать через дополнительную проверку в репозитории)
            pass

    async def transform(
        self, id: int, dto: AcademyGroupUpdateDTO, file: UploadFile | None = None
    ) -> None:
        """
        Преобразование и подготовка модели для обновления.

        Args:
            id (int): Идентификатор группы академии.
            dto (AcademyGroupUpdateDTO): Данные для преобразования.
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
            self.upload_folder = (
                f"{AppFileExtensionConstants.FieldFolderName}/academy_groups/{value}"
            )

            # Сохраняем новый файл
            file_entity = await self.file_service.save_file(
                file, self.upload_folder, self.extensions
            )
            dto.image_id = file_entity.id
