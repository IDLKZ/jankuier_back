from pydantic import BaseModel
from app.shared.dto_constants import DTOConstant


class FileDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FileCDTO(BaseModel):
    filename: DTOConstant.StandardVarcharField(description="Имя файла")
    file_path: DTOConstant.StandardTextField(description="Путь к файлу")
    file_size: DTOConstant.StandardIntegerField(description="Размер файла в байтах")
    content_type: DTOConstant.StandardVarcharField(description="MIME тип файла")
    is_remote: DTOConstant.StandardBooleanFalseField(description="Хранится ли файл удаленно")

    class Config:
        from_attributes = True


class FileRDTO(FileDTO):
    filename: DTOConstant.StandardVarcharField(description="Имя файла")
    file_path: DTOConstant.StandardTextField(description="Путь к файлу")
    file_size: DTOConstant.StandardIntegerField(description="Размер файла в байтах")
    content_type: DTOConstant.StandardVarcharField(description="MIME тип файла")
    is_remote: DTOConstant.StandardBooleanFalseField(description="Хранится ли файл удаленно")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class FileUploadResponseDTO(FileRDTO):
    """DTO для ответа после загрузки файла с дополнительной информацией"""
    url: DTOConstant.StandardTextField(description="URL для доступа к файлу")

    class Config:
        from_attributes = True