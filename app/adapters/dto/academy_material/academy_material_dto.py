from pydantic import BaseModel
from app.adapters.dto.academy.academy_dto import AcademyRDTO
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class AcademyMaterialDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyMaterialCDTO(BaseModel):
    title: DTOConstant.StandardVarcharField(description="Название материала")
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID группы (опционально)"
    )
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID файла материала"
    )

    class Config:
        from_attributes = True


class AcademyMaterialRDTO(AcademyMaterialDTO):
    title: DTOConstant.StandardVarcharField(description="Название материала")
    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID группы (опционально)"
    )
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID файла материала"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class AcademyMaterialWithRelationsRDTO(AcademyMaterialRDTO):
    academy: AcademyRDTO | None = None
    group: AcademyGroupRDTO | None = None
    file: FileRDTO | None = None

    class Config:
        from_attributes = True


class AcademyMaterialBulkCDTO(BaseModel):
    """DTO для массового создания материалов академии"""

    academy_id: DTOConstant.StandardUnsignedIntegerField(description="ID академии")
    group_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID группы (опционально)"
        )
        | None
    ) = None
    materials: list[dict] = (
        []
    )  # [{"title": "Material 1", "file_id": 1}, {"title": "Material 2", "file_id": 2}]

    class Config:
        from_attributes = True


class AcademyMaterialUpdateDTO(BaseModel):
    """DTO для обновления материала академии"""

    title: DTOConstant.StandardVarcharField(description="Название материала") | None = (
        None
    )
    group_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(description="ID группы") | None
    ) = None
    file_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID файла материала"
        )
        | None
    ) = None

    class Config:
        from_attributes = True
