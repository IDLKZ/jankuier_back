from pydantic import BaseModel
from app.adapters.dto.student.student_dto import StudentRDTO
from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupRDTO
from app.shared.dto_constants import DTOConstant


class RequestToAcademyGroupDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class RequestToAcademyGroupCDTO(BaseModel):
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    checked_by: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID пользователя, проверившего заявку"
    )
    status: DTOConstant.StandardIntegerField(
        description="Статус заявки: 0-не просмотрена, 1-принята, -1-отклонена"
    )
    info: DTOConstant.StandardNullableTextField(
        description="Дополнительная информация о заявке"
    )

    class Config:
        from_attributes = True


class RequestToAcademyGroupRDTO(RequestToAcademyGroupDTO):
    student_id: DTOConstant.StandardUnsignedIntegerField(description="ID студента")
    group_id: DTOConstant.StandardUnsignedIntegerField(description="ID группы академии")
    checked_by: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID пользователя, проверившего заявку"
    )
    status: DTOConstant.StandardIntegerField(
        description="Статус заявки: 0-не просмотрена, 1-принята, -1-отклонена"
    )
    info: DTOConstant.StandardNullableTextField(
        description="Дополнительная информация о заявке"
    )

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class RequestToAcademyGroupWithRelationsRDTO(RequestToAcademyGroupRDTO):
    student: StudentRDTO | None = None
    group: AcademyGroupRDTO | None = None

    class Config:
        from_attributes = True


class RequestToAcademyGroupUpdateDTO(BaseModel):
    """DTO для обновления заявки в группу академии"""

    checked_by: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID пользователя, проверившего заявку"
        )
        | None
    ) = None
    status: (
        DTOConstant.StandardIntegerField(
            description="Статус заявки: 0-не просмотрена, 1-принята, -1-отклонена"
        )
        | None
    ) = None
    info: (
        DTOConstant.StandardNullableTextField(
            description="Дополнительная информация о заявке"
        )
        | None
    ) = None

    class Config:
        from_attributes = True


class RequestToAcademyGroupBulkUpdateDTO(BaseModel):
    """DTO для массового обновления статуса заявок"""

    request_ids: list[
        DTOConstant.StandardUnsignedIntegerField(description="ID заявки")
    ] = []
    checked_by: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID пользователя, проверившего заявки"
    )
    status: DTOConstant.StandardIntegerField(
        description="Статус заявок: 0-не просмотрена, 1-принята, -1-отклонена"
    )

    class Config:
        from_attributes = True


