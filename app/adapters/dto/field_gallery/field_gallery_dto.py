from pydantic import BaseModel
from app.adapters.dto.field.field_dto import FieldRDTO
from app.adapters.dto.field_party.field_party_dto import FieldPartyRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class FieldGalleryDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class FieldGalleryCDTO(BaseModel):
    field_id: DTOConstant.StandardUnsignedIntegerField(description="ID поля")
    party_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID площадки (опционально)"
    )
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID файла изображения"
    )

    class Config:
        from_attributes = True


class FieldGalleryRDTO(FieldGalleryDTO):
    field_id: DTOConstant.StandardUnsignedIntegerField(description="ID поля")
    party_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID площадки (опционально)"
    )
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID файла изображения"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class FieldGalleryWithRelationsRDTO(FieldGalleryRDTO):
    field: FieldRDTO | None = None
    party: FieldPartyRDTO | None = None
    file: FileRDTO | None = None

    class Config:
        from_attributes = True


class FieldGalleryBulkCDTO(BaseModel):
    """DTO для массового создания изображений галереи поля"""

    field_id: DTOConstant.StandardUnsignedIntegerField(description="ID поля")
    party_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID площадки (опционально)"
        )
        | None
    ) = None
    file_ids: list[
        DTOConstant.StandardUnsignedIntegerField(description="ID файла изображения")
    ] = []

    class Config:
        from_attributes = True


class FieldGalleryUpdateDTO(BaseModel):
    """DTO для обновления изображения в галерее поля"""

    party_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(description="ID площадки")
        | None
    ) = None
    file_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID файла изображения"
        )
        | None
    ) = None

    class Config:
        from_attributes = True
