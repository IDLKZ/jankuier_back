import typing
from typing import Any

from starlette.datastructures import UploadFile


class AppFileExtensionConstants:
    """
    Управляет расширениями, папками типами файлов и проверкой файлов
    """

    UserFolderName = "users"
    FieldFolderName = "fields"
    ProductFolderName = "products"
    RequestMaterialFolderName = "request_materials"

    # Расширения для изображений
    IMAGE_EXTENSIONS: typing.ClassVar = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        ".tiff",
        ".ico",
        ".heic",
    }

    # Расширения для видео
    VIDEO_EXTENSIONS: typing.ClassVar = {
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".flv",
        ".wmv",
        ".webm",
        ".mpeg",
        ".3gp",
        ".m4v",
    }

    # Расширения для аудио
    AUDIO_EXTENSIONS: typing.ClassVar = {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
        ".m4a",
        ".wma",
        ".amr",
        ".opus",
        ".aiff",
    }

    # Расширения для документов
    DOCUMENT_EXTENSIONS: typing.ClassVar = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".csv",
        ".rtf",
        ".odt",
        ".ods",
        ".odp",
        ".epub",
        ".pages",
        ".numbers",
        ".key",
    }

    # Расширения для архивов
    ARCHIVE_EXTENSIONS: typing.ClassVar = {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".iso",
        ".tgz",
        ".tar.gz",
    }

    # Расширения для текстовых файлов
    TEXT_EXTENSIONS: typing.ClassVar = {
        ".txt",
        ".log",
        ".md",
        ".yaml",
        ".yml",
        ".json",
        ".xml",
        ".html",
        ".css",
        ".js",
    }

    # Расширения для документов оплаты
    PAYMENT_DOCUMENT_EXTENSIONS: typing.ClassVar = {".jpg", ".jpeg", ".png", ".pdf"}

    # Все расширения
    ALL_EXTENSIONS = (
        IMAGE_EXTENSIONS
        | VIDEO_EXTENSIONS
        | AUDIO_EXTENSIONS
        | DOCUMENT_EXTENSIONS
        | ARCHIVE_EXTENSIONS
        | TEXT_EXTENSIONS
    )

    @staticmethod
    def is_valid_extension(extension: str, allowed_extensions: set) -> bool:
        """
        Проверяет, является ли расширение файла допустимым.

        Args:
            extension (str): Расширение файла (например, '.jpg').
            allowed_extensions (set): Набор допустимых расширений.

        Returns:
            bool: True, если расширение допустимо, иначе False.
        """
        return extension.lower() in allowed_extensions

    @staticmethod
    def is_upload_file(obj: Any) -> bool:  # noqa:ANN401
        return isinstance(obj, UploadFile)

    @staticmethod
    def user_profile_photo_directory(username: str) -> str:
        return "users/photos/" + username

    @staticmethod
    def field_image_directory(field_value: str) -> str:
        return "fields/images/" + field_value

    @staticmethod
    def product_image_directory(product_value: str) -> str:
        return "products/images/" + product_value

    @staticmethod
    def application_document_directory(id: int, department_str: str) -> str:
        return "applications/documents/" + f"{id}/{department_str}"

    @staticmethod
    def request_material_directory(request_id: int, student_id: int) -> str:
        return f"request_materials/{request_id}/{student_id}"
