import base64
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_exception_response import AppExceptionResponse
from app.entities import FileEntity
from app.i18n.i18n_wrapper import i18n
from app.infrastructure.app_config import app_config
from app.shared.app_file_constants import AppFileExtensionConstants


class FileService:
    """📌 Сервис работы с файлами"""

    UPLOAD_FOLDER = f"{app_config.static_folder}/{app_config.upload_folder}"
    ALLOWED_EXTENSIONS: dict = AppFileExtensionConstants.ALL_EXTENSIONS
    NOT_ALLOWED_EXTENSIONS = app_config.not_allowed_extensions
    MAX_FILE_SIZE_MB = app_config.app_upload_max_file_size_mb

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def change_max_size(self, max_size_mb: float):
        self.MAX_FILE_SIZE_MB = max_size_mb

    @staticmethod
    def generate_file_path(filename: str, directory: str) -> str:
        """
        Генерирует уникальный путь для файла.

        :param filename: Оригинальное имя файла.
        :param directory: Директория для сохранения.
        :return: Уникальный путь к файлу.
        """
        safe_filename = f"{uuid.uuid4().hex}_{Path(filename).name}"
        return os.path.join(directory, safe_filename)

    @staticmethod
    def validate_file(file: UploadFile, extensions=None):
        """
        Проверяет размер файла и его расширение.

        :param file: Файл для проверки.
        :param extensions: Разрешенные расширения (если переданы).
        :raises AppExceptionResponse: Если файл не соответствует требованиям.
        """
        ALLOWED_EXTENSIONS = extensions or FileService.ALLOWED_EXTENSIONS

        # Проверка расширения
        _, extension = os.path.splitext(file.filename)
        if (
            extension.lower() not in ALLOWED_EXTENSIONS
            or extension.lower() in FileService.NOT_ALLOWED_EXTENSIONS
        ):
            raise AppExceptionResponse.bad_request(
                message=f"Недопустимое расширение файла. Допустимы: {list(ALLOWED_EXTENSIONS)}"
            )

        # Проверка размера
        file.file.seek(0, os.SEEK_END)
        file_size_mb = file.file.tell() / (1024 * 1024)
        file.file.seek(0)  # Возврат указателя файла в начало
        if file_size_mb > FileService.MAX_FILE_SIZE_MB:
            raise AppExceptionResponse.bad_request(
                message=f"Файл слишком большой. Максимальный размер: {FileService.MAX_FILE_SIZE_MB} МБ"
            )

    async def save_file(
        self, file: UploadFile, uploaded_folder: str, extensions: Optional[dict] = None
    ) -> FileEntity:
        """
        Сохраняет файл в статичной папке и создает запись в базе данных.

        :param file: Загружаемый файл.
        :param uploaded_folder: Папка для загрузки.
        :param extensions: Допустимые расширения (если переданы).
        :return: Модель сохраненного файла.
        """
        # try:
        FileService.validate_file(file, extensions)

        upload_directory = os.path.join(FileService.UPLOAD_FOLDER, uploaded_folder)
        os.makedirs(upload_directory, exist_ok=True)

        file_path = FileService.generate_file_path(file.filename, upload_directory)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        file_record = FileEntity(
            filename=file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            content_type=file.content_type,
        )
        self.db.add(file_record)
        await self.db.commit()
        await self.db.refresh(file_record)
        return file_record

    # except Exception as exc:
    #     await self.db.rollback()
    #     raise AppExceptionResponse.internal_error(
    #         message="Ошибка при сохранении файла",
    #         extra={"filename": file.filename, "details": str(exc)},
    #         is_custom=True,
    #     )

    async def delete_file(self, file_id: int) -> bool:
        """
        Удаляет файл с диска и из базы данных.

        :param file_id: ID файла.
        :param db: Сессия базы данных.
        :return: True, если файл удален, иначе False.
        """
        try:
            file_record = await self.db.get(FileEntity, file_id)
            if not file_record:
                return False

            if os.path.exists(file_record.file_path):
                os.remove(file_record.file_path)

            await self.db.delete(file_record)
            await self.db.commit()
            return True
        except Exception as exc:
            await self.db.rollback()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("file_delete_error"),
                extra={"file_id": file_id, "details": str(exc)},
                is_custom=True,
            )

    async def update_file(
        self,
        file_id: int,
        new_file: UploadFile,
        uploaded_folder: str,
        extensions: Optional[dict] = None,
    ) -> FileEntity:
        """
        Обновляет файл на диске и запись в базе данных.

        :param file_id: ID файла.
        :param new_file: Новый файл.
        :param uploaded_folder: Папка для загрузки.
        :param extensions: Разрешенные расширения (если переданы).
        :return: Обновленная модель файла.
        """
        try:
            existing_file = await self.db.get(FileEntity, file_id)
            if not existing_file:
                raise AppExceptionResponse.bad_request(message=i18n.gettext("file_not_found"))

            if os.path.exists(existing_file.file_path):
                os.remove(existing_file.file_path)

            FileService.validate_file(new_file, extensions)

            upload_directory = os.path.join(FileService.UPLOAD_FOLDER, uploaded_folder)
            os.makedirs(upload_directory, exist_ok=True)

            new_file_path = FileService.generate_file_path(
                new_file.filename, upload_directory
            )

            with open(new_file_path, "wb") as f:
                f.write(await new_file.read())

            existing_file.filename = new_file.filename
            existing_file.file_path = new_file_path
            existing_file.file_size = os.path.getsize(new_file_path)
            existing_file.content_type = new_file.content_type
            await self.db.commit()
            await self.db.refresh(existing_file)
            return existing_file
        except Exception as exc:
            await self.db.rollback()
            raise AppExceptionResponse.internal_error(
                message=i18n.gettext("file_update_error"),
                extra={"file_id": file_id, "details": str(exc)},
                is_custom=True,
            )

    async def read_file_base64(self, file_id: int) -> str:
        """
        Читает файл из хранилища и возвращает его в кодировке Base64.

        :param file_id: ID файла в базе данных.
        :return: Строка Base64 с содержимым файла.
        """
        file_record = await self.db.get(FileEntity, file_id)
        if not file_record or not os.path.exists(file_record.file_path):
            raise AppExceptionResponse.bad_request(message="Файл не найден")

        try:
            with open(file_record.file_path, "rb") as f:
                encoded_file = base64.b64encode(f.read()).decode("utf-8")
            return encoded_file
        except Exception as e:
            raise AppExceptionResponse.internal_error(
                message=f"{i18n.gettext('file_read_error')}: {str(e)}"
            )

    async def get_full_file_path(self, file_id: int) -> str:
        """
        Возвращает полный путь к файлу.

        :param file_id: ID файла.
        :return: Полный путь к файлу.
        """
        file_record = await self.db.get(FileEntity, file_id)
        if not file_record:
            raise AppExceptionResponse.bad_request(message="Файл не найден")

        return file_record.file_path

    async def save_from_bytes(
        self, file_bytes: bytes, filename: str, uploaded_folder: str
    ) -> FileEntity:
        """
        Декодирует строку Base64 (или bytes) и сохраняет файл.

        :param db: Асинхронная сессия базы данных.
        :param base64_str: Данные Base64 (строка или байты).
        :param filename: Имя файла.
        :param uploaded_folder: Папка для загрузки.
        :return: Объект FileEntity.
        """
        try:

            # ✅ Создаём папку, если её нет
            upload_directory = os.path.join(
                app_config.static_folder, app_config.upload_folder, uploaded_folder
            )
            os.makedirs(upload_directory, exist_ok=True)

            # ✅ Генерируем уникальное имя файла
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(upload_directory, unique_filename)

            # ✅ Сохраняем файл (ПРЯМО ИЗ `bytes`)
            with open(file_path, "wb") as file:
                file.write(file_bytes)

            # ✅ Определяем MIME-тип (по расширению)
            content_type = (
                "application/pdf"
                if filename.endswith(".pdf")
                else "application/octet-stream"
            )

            # ✅ Создаём запись в БД
            file_record = FileEntity(
                filename=filename,
                file_path=file_path,
                file_size=len(file_bytes),
                content_type=content_type,
            )
            self.db.add(file_record)
            await self.db.commit()
            await self.db.refresh(file_record)

            return file_record

        except Exception as e:
            await self.db.rollback()
            raise AppExceptionResponse.internal_error(
                message="Ошибка при сохранении файла из Base64",
                extra={"filename": filename, "details": str(e)},
                is_custom=True,
            )
