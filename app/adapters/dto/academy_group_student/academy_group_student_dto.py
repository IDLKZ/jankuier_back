from pydantic import BaseModel
from app.adapters.dto.student.student_dto import StudentRDTO
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.adapters.dto.request_to_academy_group.request_to_academy_group_dto import (
    RequestToAcademyGroupRDTO,
)
from app.adapters.dto.base_pagination_dto import BasePageModel
from app.shared.dto_constants import DTOConstant


class AcademyGroupStudentDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class AcademyGroupStudentCDTO(BaseModel):
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    request_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID заявки (если студент был добавлен через заявку)"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность студента в группе"
    )
    info: DTOConstant.StandardNullableTextField(description="Дополнительная информация")

    class Config:
        from_attributes = True


class AcademyGroupStudentRDTO(AcademyGroupStudentDTO):
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    request_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID заявки (если студент был добавлен через заявку)"
    )
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность студента в группе"
    )
    info: DTOConstant.StandardNullableTextField(description="Дополнительная информация")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class AcademyGroupStudentWithRelationsRDTO(AcademyGroupStudentRDTO):
    student: StudentRDTO | None = None
    group: AcademyGroupRDTO | None = None
    request: RequestToAcademyGroupRDTO | None = None

    class Config:
        from_attributes = True


class AcademyGroupStudentUpdateDTO(BaseModel):
    """DTO для обновления студента в группе"""

    is_active: (
        DTOConstant.StandardBooleanTrueField(description="Активность студента в группе")
        | None
    ) = None
    info: (
        DTOConstant.StandardNullableTextField(description="Дополнительная информация")
        | None
    ) = None

    class Config:
        from_attributes = True


class AcademyGroupStudentBulkCDTO(BaseModel):
    """DTO для массового добавления студентов в группу"""

    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    students: list[dict] = []  # [{"student_id": 1, "request_id": None, "info": ""}]

    class Config:
        from_attributes = True


class AcademyGroupStudentBulkUpdateDTO(BaseModel):
    """DTO для массового обновления статуса студентов в группе"""

    student_ids: list[
        DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    ] = []
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    is_active: DTOConstant.StandardBooleanTrueField(
        description="Активность студентов в группе"
    )

    class Config:
        from_attributes = True


class PaginationAcademyGroupStudentRDTO(BasePageModel):
    items: list[AcademyGroupStudentRDTO]


class PaginationAcademyGroupStudentWithRelationsRDTO(BasePageModel):
    items: list[AcademyGroupStudentWithRelationsRDTO]
