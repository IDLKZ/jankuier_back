from pydantic import BaseModel
from app.adapters.dto.academy.academy_dto import AcademyRDTO
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class AcademyGalleryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyGalleryCDTO(BaseModel):
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID группы (опционально)")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения")

    class Config:
        from_attributes = True


class AcademyGalleryRDTO(AcademyGalleryDTO):
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID группы (опционально)")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class AcademyGalleryWithRelationsRDTO(AcademyGalleryRDTO):
    academy: AcademyRDTO | None = None
    group: AcademyGroupRDTO | None = None
    file: FileRDTO | None = None

    class Config:
        from_attributes = True


class AcademyGalleryBulkCDTO(BaseModel):
    """DTO для массового создания изображений галереи академии"""
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID группы (опционально)") | None = None
    file_ids: list[DTOConstant.StandardUnsignedIntegerField(description="ID файла изображения")] = []

    class Config:
        from_attributes = True


class AcademyGalleryUpdateDTO(BaseModel):
    """DTO для обновления изображения в галерее академии"""
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID группы") | None = None
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла изображения") | None = None

    class Config:
        from_attributes = True