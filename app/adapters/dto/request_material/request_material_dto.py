from pydantic import BaseModel
from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import RequestToAcademyGroupRDTO
from app.adapters.dto.student.student_dto import StudentRDTO
from app.adapters.dto.file.file_dto import FileRDTO
from app.shared.dto_constants import DTOConstant


class RequestMaterialDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class RequestMaterialCDTO(BaseModel):
    title: DTOConstant.StandardVarcharField(description="Название материала запроса")
    request_id: DTOConstant.StandardUnsignedIntegerField(description="ID заявки в группу")
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла материала")

    class Config:
        from_attributes = True


class RequestMaterialRDTO(RequestMaterialDTO):
    title: DTOConstant.StandardVarcharField(description="Название материала запроса")
    request_id: DTOConstant.StandardUnsignedIntegerField(description="ID заявки в группу")
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла материала")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class RequestMaterialWithRelationsRDTO(RequestMaterialRDTO):
    request: RequestToAcademyGroupRDTO | None = None
    student: StudentRDTO | None = None
    file: FileRDTO | None = None

    class Config:
        from_attributes = True


class RequestMaterialBulkCDTO(BaseModel):
    """DTO для массового создания материалов запроса"""
    request_id: DTOConstant.StandardUnsignedIntegerField(description="ID заявки в группу")
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    materials: list[dict] = []  # [{"title": "Material 1", "file_id": 1}, {"title": "Material 2", "file_id": 2}]

    class Config:
        from_attributes = True


class RequestMaterialUpdateDTO(BaseModel):
    """DTO для обновления материала запроса"""
    title: DTOConstant.StandardVarcharField(description="Название материала запроса") | None = None
    file_id: DTOConstant.StandardNullableUnsignedIntegerField(description="ID файла материала") | None = None

    class Config:
        from_attributes = True